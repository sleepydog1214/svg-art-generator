import argparse

class Setup:
    
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("file", help="Input .jpg, .jpeg, or .png file")
        
    def GetArgs(self):
        args = self.parser.parse_args()
        return self.getUserFile(args.file)
        
    # ******************************************************************************
    # getUserFile() - Validate, then get, the name of the input image
    # *****************************************************************************
    def getUserFile(self, name):
        "This gets the name of the image file to process."
        try:
            tmp = name.lower()

            # file must be a jpeg or png file
            if not tmp.endswith('.jpg') and \
            not tmp.endswith('.jpeg') and \
            not tmp.endswith('.png'):
                raise IOError

        except IOError:
            print("Input IO error (file must be jpg or png)")
            sys.exit(1)

        return name
                
        