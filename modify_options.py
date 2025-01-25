import json

def recall_current_configuration(configuration_file:str) -> dict:
        """Summary --> Retrieves presentation preferences from config.json. Returns data as a dictionary.
            Returns --> (dict) : A set of key word pairs indicating the current option selection."""
        with open(configuration_file) as json_file:
            config_information = json.load(json_file)
            return config_information

def display_settings(configuration):
    for group in configuration:
        print(group)
        for setting in configuration[group]:
            if configuration[group] == configuration['sources']:   
                for source in configuration[group]:
                    for attribute in source:
                        print(f"    {attribute} : {source[attribute]}")
            else:
                print(f"    {setting} : {configuration[group][setting]}")
        print()
    
    

# --- THIS DOWN HERE IS THE SHIT --- #

def change_config(options_local_copy:dict, configuration_file:str ,target_setting:str, new_value):
    options_local_copy[target_setting]=new_value
    
    outgoing_config = json.dumps(options_local_copy, indent=4)
    with open(configuration_file, 'w') as json_file:
        json_file.write(outgoing_config)
        
    # I have no idea what is going on tbh. suffer future dena
def main():
    current_configuration = recall_current_configuration("copy.json")
    display_settings(current_configuration)
    change_config(current_configuration, "copy.json", "Toggle TTS", True)
    display_settings(current_configuration)
    
if __name__ == "__main__":
    main()