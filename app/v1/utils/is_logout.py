#!/usr/bin/env python3

blacklisted_tokens = set()

def blacklist_token(token):
    """this function impelements blacklist of a token"""
    blacklisted_tokens.add(token)

def log_out_token(token):
    """check if token is in blacklist set"""
    if not blacklist_token(token):
          return False

print(blacklisted_tokens)