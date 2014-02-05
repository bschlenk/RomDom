#!/usr/bin/env python

"""
Coolrom Explorer
================
Browse and download roms from coolrom.com, bypassing the annoying 15 second wait time

Script and download multiple files
"""

# Standard Libarary imports
import sys, os
import urllib2
import urlparse
import argparse
import re

# RomDom Library imports
from romdom.system import System
from romdom import urls
from romdom import util
from romdom import get_system_list

###############################################################################

def parse_args():
	parser = argparse.ArgumentParser(description='Download roms from various locations, from the command line.')
	parser.add_argument('-s', '--system', help='the game system you would like to find a rom for')
	parser.add_argument('--search', action='store_true', help='search various rom websites')
	parser.add_argument('query', help='the search terms to use when searching for roms')
	parser.add_argument('-d', '--download', action='store_true', help='download the rom given by the query term')
	return parser.parse_args()	

###############################################################################	
	
def main():
	args = parse_args()
	systems = get_system_list()

	if args.search:
		if not args.system:
			print 'you must specify a system with --system SYSTEM'
			sys.exit(1)
		try:
			roms = systems[args.system].search(args.query)
		except KeyError:
			print 'invalid system - valid options are [\n\t%s\n]' % '\n\t'.join(systems.keys())
			sys.exit(2)
		for r in roms:
			print r
		sys.exit(0)

	if args.download:
		if args.system:
			rom = systems[args.system].get_rom(args.query)
		else:
			for s in systems.values():
				rom = s.get_rom(args.query)
				if rom:
					break
		if rom:
			rom.download()
		else:
			print 'could not find a rom called "%s"' % args.query
		sys.exit(0)
			
	#print 'available systems:'
	#print '\n'.join(zip(*systems)[0])
	
	#print systems.keys()
	#mario = systems['Nintendo'].get_rom('Super Mario Bros.')
	#mario.download('%s.zip' % mario.name)
	

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "\nexiting"
		
