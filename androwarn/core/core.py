#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Global imports
import re, logging

# Androguard imports
from androguard.core.analysis.analysis import *

# Androwarn modules import
from androwarn.constants.api_constants import *

# Constants 
ERROR_VALUE_NOT_FOUND = 'N/A'
ERROR_CONSTANT_NAME_NOT_FOUND = 'N/A'

CONST_STRING = 'const-string'
CONST = 'const'
MOVE = 'move'
MOVE_RESULT = 'move-result'
APUT = 'aput'
INVOKE = 'invoke'
INVOKE_NO_REGISTER = 'invoke-no-register'
INVOKE_2_REGISTERS = 'invoke-2-registers'
NEW_INSTANCE = 'new-instance'

# Logguer
log = logging.getLogger('log')

# Instruction matcher
def match_current_instruction(current_instruction, registers_found) :
		#regexes
		p_const 				= re.compile('^const(?:\/4|\/16|\/high16|-wide(?:\/16|\/32)|-wide\/high16|)? v([0-9]+) , (?:.*) // \{(\-?[0-9]+(?:\.[0-9]+)?)\}$')
		p_const_string			= re.compile('^const-string(?:||-jumbo) v([0-9]+) , \[ string@ (?:[0-9]+) \'(.*)\' \]$')
		p_move					= re.compile('move(?:|\/from16|-wide(?:\/from16|\/16)|-object(?:|\/from16|\/16))? v([0-9]+) , (v[0-9]+)')
		p_move_result			= re.compile('move(?:-result(?:|-wide|-object)|-exception)? v([0-9]+)')
		p_aput					= re.compile('^aput(?:-wide|-object|-boolean|-byte|-char|-short|) v([0-9]+) , v([0-9]+) , v([0-9]+)$')
		p_invoke 				= re.compile('^invoke-(?:static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick) v([0-9]+) , \[ meth@ (?:[0-9]+) (L(?:.*); .*) \[(.*)\] \]$')
		p_invoke_2_registers 	= re.compile('^invoke-(?:static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick) v([0-9]+) , v([0-9]+) , \[ meth@ (?:[0-9]+) (L(?:.*); .*) \[(.*)\] \]$')
		p_invoke_no_register	= re.compile('^invoke-(?:static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick) \[ meth@ (?:[0-9]+) (L(?:.*); .*) \[(.*)\] \]$')
		p_new_instance 			= re.compile('^new-instance v([0-9]+) , \[ type@ (?:[0-9]+) (L(?:.*);) \]$')
		
		
		# Returned values init
		instruction_name = ''
		local_register_number = -1
		local_register_value = -1
		
		
		if p_const_string.match(current_instruction) :
			#print p_const_string.match(current_instruction).groups()
			
			instruction_name = CONST_STRING
			
			register_number = p_const_string.match(current_instruction).groups()[0]
			register_value = p_const_string.match(current_instruction).groups()[1]
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value
			else :
				old_string = registers_found[register_number]
				new_string = "%s %s" % (str(register_value), str(old_string))
				registers_found[register_number] = new_string
			
			local_register_number = register_number
			local_register_value = register_value
	
	
		if p_const.match(current_instruction) :
			#print p_const.match(current_instruction).groups()
			
			instruction_name = CONST
			
			register_number = p_const.match(current_instruction).groups()[0]
			register_value = p_const.match(current_instruction).groups()[1]
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value
			
			local_register_number = register_number
			local_register_value = register_value
	
	
		if p_move.match(current_instruction) :
			#print p_move.match(current_instruction).groups()
			
			instruction_name = MOVE
			
			register_number = p_move.match(current_instruction).groups()[0]
			register_value = p_move.match(current_instruction).groups()[1]
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value				
			
			local_register_number = register_number
			local_register_value = register_value


		if p_move_result.match(current_instruction) :
			#print p_move_result.match(current_instruction).groups()
			
			instruction_name = MOVE_RESULT
			
			register_number = p_move_result.match(current_instruction).groups()[0]
			register_value = ''
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value		
			
			local_register_number = register_number
			local_register_value = register_value	
			#print "number returned %s" % local_register_number
			#print "value returned %s" % local_register_value	

		if p_invoke.match(current_instruction) :
			#print p_invoke.match(current_instruction).groups()
			
			instruction_name = INVOKE
			
			register_number = p_invoke.match(current_instruction).groups()[0]
			register_value = p_invoke.match(current_instruction).groups()[1]
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value		
			
			local_register_number = register_number
			local_register_value = register_value		
		
		if p_invoke_no_register.match(current_instruction) :
			#print p_invoke.match(current_instruction).groups()
			
			instruction_name = INVOKE_NO_REGISTER
			
			register_number = ''
			register_value = p_invoke_no_register.match(current_instruction).groups()[0]
			
			local_register_number = register_number
			local_register_value = register_value
		
		if p_invoke_2_registers.match(current_instruction) :
			#print p_invoke.match(current_instruction).groups()
			
			instruction_name = INVOKE_NO_REGISTER
			
			register_number = p_invoke_2_registers.match(current_instruction).groups()[0]
			register_value = p_invoke_2_registers.match(current_instruction).groups()[1]
			
			local_register_number = register_number
			local_register_value = register_value		
			
		if p_new_instance.match(current_instruction) :
			#print p_new_instance.match(current_instruction).groups()
			
			instruction_name = INVOKE
			
			register_number = p_new_instance.match(current_instruction).groups()[0]
			register_value = p_new_instance.match(current_instruction).groups()[1]
			
			if not(register_number in registers_found) :
				registers_found[register_number] = register_value		
			
			local_register_number = register_number
			local_register_value = register_value
		
		if p_aput.match(current_instruction) :
			#print p_aput.match(current_instruction).groups()
			
			instruction_name = APUT
			
			register_object_reference = p_aput.match(current_instruction).groups()[0]
			register_array_reference = p_aput.match(current_instruction).groups()[1]
			register_element_index = p_aput.match(current_instruction).groups()[2]

			local_register_number = register_object_reference 
			local_register_value =  register_array_reference	
			#supprimer dans relevant_registers la valeur 'array_reference'
			
			#ajouter object_reference
			#modifier la condition d'ajout pour "const_string" pour le cas ou il y a déja ce même numéro de registre => concaténer les valeurs en LIFO strcat(%s%s,new_element, old_string)
		
		return instruction_name, local_register_number, local_register_value, registers_found	

# Backtrace registers #
def find_call_index_in_code_list(index_to_find, instruction_list):
	"""
	@param index_to_find : index of the method call
	@param code_list : instruction list of the parent method called
	
	@rtype : the index of the method call in the instruction listing
	"""	
	idx = 0
	for i in instruction_list :
		if index_to_find <= idx :
			#print "[+] code offset found at the index " + str(instruction_list.index(i))
			return instruction_list.index(i)
		else :
			idx += i.get_length()
	
	# in case of failure, return an inconsistent value
	return ERROR_INDEX_NOT_FOUND

def backtrace_registers_before_call(x, method, index_to_find) :
	"""
	@param x : a VMAnalysis instance
	@param method : a regexp for the method (the package)
	@param index_to_find : index of the matching method
	
	@rtype : an ordered list of dictionaries of each register content [{ 'register #': 'value' }, { 'register #': 'value' } ...]
	"""	
	registers = {}
	
	code = method.get_code()
	#code.show()
	
	bc = code.get_bc()
	instruction_list = bc.get()
	

	found_index = find_call_index_in_code_list(index_to_find, instruction_list)
	
	if (found_index < 0) :
		log.error("The call index in the code list can not be found")
		return 0
		
	else :
		# Initialize the returned list of dictionaries
		registers_final = []
		
		# Initialize the harvesting dictionary
		registers_found = {}
		
		# List the register indexes related to the method call
		relevant_registers = relevant_registers_for_the_method(method, index_to_find)
		#print relevant_registers
		
		i = int(found_index) - 1 # start index
		

		while ((all_relevant_registers_filled(registers_found,relevant_registers) != True) and (i >= 0)) :
			current_instruction = instruction_list[i].show_buff(0)
			#print current_instruction
			
			instruction_name, local_register_number, local_register_value, registers_found =  match_current_instruction(current_instruction, registers_found)
			
			if cmp(instruction_name, APUT) == 0:
				try :
					list_index_to_be_changed = relevant_registers.index(str(local_register_value))
					#print "index_to_be_changed %s" % list_index_to_be_changed
					del(relevant_registers[int(local_register_value)]) 
					relevant_registers.insert(list_index_to_be_changed, local_register_number)
					log.info("New relevant_registers %s" % relevant_registers)
				except :
					log.warn("'%s' does not exist anymore in the relevant_registers list" % local_register_value)
			
			if (cmp(instruction_name, MOVE_RESULT) == 0) and (local_register_number in relevant_registers):
				try:
					past_instruction = instruction_list[i-1].show_buff(0)
					p_instruction_name, p_local_register_number, p_local_register_value, registers_found =  match_current_instruction(past_instruction, registers_found)
					
					#print past_instruction
					if cmp(p_instruction_name, INVOKE_NO_REGISTER) == 0 :
						registers_found[local_register_number] = p_local_register_value
					
					else:
						list_index_to_be_changed = relevant_registers.index(str(local_register_number))
						del(relevant_registers[int(list_index_to_be_changed)])
						relevant_registers.insert(list_index_to_be_changed, p_local_register_number)
					
					log.info("New relevant_registers %s" % relevant_registers)
				
				except:
					log.warn("'%s' does not exist anymore in the relevant_registers list" % local_register_value)

			i = i - 1
		
		#log.info('Registers found during the analysis %s' % registers_found)
			
			
		
		final_answer = all_relevant_registers_filled(registers_found,relevant_registers)
		log.info("Are all relevant registers filled ? %s" % str(final_answer))
		
		for i in relevant_registers :			
			try:
				register_number	= i
				#print register_number
				
				register_value 	= registers_found[i]
				#print register_value
				
				temp_dict = { register_number : register_value }
				registers_final.append(temp_dict)
			
			except KeyError:
				registers_final = []
				log.warn("KeyError exception : The value of the register # %s could not be found for the relevant registers %s" % (register_number, relevant_registers))
				break
				
		
		
		return registers_final

		
def extract_register_index_out_splitted_values(registers_raw_list_splitted) :
	"""
	@param : registers_raw_list_splitted : a list of registers still containing the 'v' prefix [' v1 ', ' v2 ' ...]
	
	@rtype : an ordered list of register indexes ['1', '2' ...]
	"""		
	relevant_registers = []
	
	# Trim the values
	registers_raw_list_splitted[:] = (value.strip() for value in registers_raw_list_splitted if len(value) > 0)
	
	for value in registers_raw_list_splitted :
		
		# Remove that 'v'
		p_register_index_out_of_split = re.compile('^v([0-9]+)$')
		
		if p_register_index_out_of_split.match(value) :
			#print p_register_index_out_of_split.match(value).groups()
			register_index = p_register_index_out_of_split.match(value).groups()[0]
			
			relevant_registers.append(register_index)
		
		else :
			relevant_registers.append('N/A')
	
	return relevant_registers


def relevant_registers_for_the_method(method, index_to_find) :
	"""
	@param method : a method instance
	@param index_to_find : index of the matching method
	
	@rtype : an ordered list of register indexes related to that method call
	"""	
	relevant_registers = []
	
	code = method.get_code()
	#code.show()
	
	bc = code.get_bc()
	instruction_list = bc.get()
	

	found_index = find_call_index_in_code_list(index_to_find, instruction_list)
	
	if (found_index < 0) :
		log.error("The call index in the code list can not be found")
		return 0
		
	else :
		current_instruction = instruction_list[found_index].show_buff(0)
		#print current_instruction
	
		p_invoke = re.compile('^invoke-(static|virtual|direct|super|interface|interface-range|virtual-quick|super-quick)(?:\/range)? (v(.+) ,)+ \[(?:(.*))$')
		
		if p_invoke.match(current_instruction) :
			registers_raw_list_splitted = p_invoke.match(current_instruction).groups()[1].split(',')
			relevant_registers = extract_register_index_out_splitted_values(registers_raw_list_splitted)
		
		# -- OLD --
		#Delete the 1st elements, as it is the method's instance register
		#relevant_registers.pop(0)
		# ---------
		
		return relevant_registers


def all_relevant_registers_filled(registers, relevant_registers) :
	"""
	@param registers : a dictionary of each register content { 'register #': 'value' }
	@param relevant_registers : an ordered list of register indexes related to that method call
	
	@rtype : True if all the relevant_registers are filled, False if not 
	"""	
	answer = True
	
	for i in relevant_registers :
		# assert a False answer for null registers from the "move-result" instruction
		if not(i in registers) or (i in registers and len(registers[i]) < 1) :
			answer = False
		'''	
		if not(i in registers) :
			answer = False
		'''
	return answer


def get_register_value(index, registers) :
	"""
	@param index : integer value of the index
	@param registers : an ordered list of register indexes related to that method call
	
	@rtype : a value casted in string
	"""
	# Index - 1, list starts at index 0
	if index <= len(registers) :
		dict = registers[index]
		#dict = registers[index-1]
		return dict.values()[0]
	else :
		return ERROR_VALUE_NOT_FOUND

def get_constants_name_from_value(constant_dict, value) :
	"""
	@param constant_dict : constant dictionary to consider
	@param value : value's constant name to retrieve
	
	@rtype : a string
	"""
	try:
		return constant_dict[value]
	
	except KeyError:
		log.error("The constant name corresponding to the value '%s' can not be found in the dictionary '%s'" % (value, constant_dict))
		return ERROR_CONSTANT_NAME_NOT_FOUND
	
	
#########################