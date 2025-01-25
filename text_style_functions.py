def style_text(msg:str, codes:str)->str:
    """Summary --> Accepts message and style codes as strings. Parses style codes to apply indicated ANSI text style options. Returns message with added ANSI codes.
        Arguments --> msg (str) : Message to be modified with ANSI style codes.
                      codes (str) : Style codes. When parsed, used to assemble ANSI style code. Sould follow format 'fXXbXX[X][UR].' 'f' and 'b' should always be in indicated positions. The Xs indicate numbers to be included following the indicating letters. 'f' should only every be followed by a two digit number, 'b' can be followed by either a two or three digit number. Valid numbers can be seen in the following lists. each number relates to an ANSI code for either foreground or background coloring. Append to the end of the code either 'U' or 'R' to underline or color invert the text respectively."""
    
    valid_foreground_code_numbers = ['30', '31', '32', '33', '34', '35', '36', '37', '39', '90', '91', '92', '93', '94', '95', '96', '97']
    valid_background_code_numbers = ['40', '41', '42', '43', '44', '45', '46', '47', '49', '100', '101', '102', '103', '104', '105', '106', '107']
    
    if ('U' in codes) and ('R' in codes):
        print("Test cannot be reversed and underlined.\nIf this needs to be done, specify foreground and background colors and include code 'U'.")
    elif 'U' in codes:
        text_style_code = ';4m'
        codes = ''.join([codes[i] for i in range(len(codes)) if i != codes.index('U')])
    elif 'R' in codes:
        text_style_code = ';7m'
        codes = ''.join([codes[i] for i in range(len(codes)) if i != codes.index('R')])
    else:
        text_style_code = 'm'
    
    if (len(codes)<6) or ((codes[0] != 'f') or (codes[3] != 'b')):
        print("\nThere is an error in the provided code.\nIt should be reviewed.\n\n")
        exit()
    elif (codes[0] == 'f') and (codes[3] == 'b'):
        code = codes
        
    foreground_code=code[1:3]
    background_code=code[4::]
    
    if  (foreground_code not in valid_foreground_code_numbers) or (background_code not in valid_background_code_numbers):
        print('These codes are invalid.')
        exit()
        
    style_code = f"[{foreground_code};{background_code}{text_style_code}"
    colored_message = f"\033{style_code}{msg}\033[0m"
    
    return colored_message