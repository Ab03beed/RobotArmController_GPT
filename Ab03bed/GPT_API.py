import os
import openai

class GPT_API:
    #default constructor
    def __init__(self):
        # Set OpenAI API key through system varibales
        openai.api_key = os.getenv("GPT_KEY")

        # Lists of possible transcriptions for each box to handle misinterpretations
        # or different pronunciations/accent variations
        self._box_1_variants = [ 
            "box one", "box 1", "box won", "barks one", "fox one", "books one",  
            "boks one", "bok one", "boxen one", "box on", "bax one", "bux one", 
            "boks ett", "bok ett", "box ett", "bex one", "bogs one", "bog one", 
            "buck one", "buck ett", "bokk one", "bokks one", "boxen ett", "box on ett", 
            "boks on", "boxen on", "bok on", "boxen won", "boxen ett", "bokks won",  
            "bokks on", "bokks ett", "bex won", "bex on", "bex ett" 
        ] 
        self._box_2_variants = [ 
            "books to","box two", "box 2", "box to", "box too", "barks two", "fox two", "books two", 
            "boks two", "bok two", "boxen two", "box tu", "bax two", "bux two", 
            "boks två", "bok två", "box två", "bex two", "bogs two", "bog two", 
            "buck two", "buck två", "bokk two", "bokks two", "boxen två", "box tu två", 
            "boks tu", "boxen tu", "bok tu", "boxen too", "boxen två", "bokks too",  
            "bokks tu", "bokks två", "bex too", "bex tu", "bex två" 
        ] 
        self._box_3_variants = [ 
            "box three", "box 3", "barks three", "fox three", "books three", 
            "boks three","books 3", "bok three", "boxen three", "box tree", "bax three", "bux three", 
            "boks tre", "bok tre", "box tre", "bex three", "bogs three", "bog three", 
            "buck three", "buck tre", "bokk three", "bokks three", "boxen tre", "box tree tre", 
            "boks tree", "boxen tree", "bok tree", "boxen trey", "boxen tre", "bokks tree",  
            "bokks trey", "bokks tre", "bex tree", "bex trey", "bex tre" 
        ] 


    def _gptCall(self, which_box):
        gpt_call = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", 
            messages=[ 

                {"role": "system", "content": "You are an experienced robot operations coder that will help the user to code a collaborative robot."}, 
                {"role": "user", "content": f""" 
                Imagine we are working with a collaborative robot with the task of moving boxes from a "pick-up table" to a "release table".  
                The three boxes is called BOX_1, BOX_2 and BOX_3. The position of boxes at the pick up table is given in XYZ coordinates: BOX_1(5,3,4), BOX_2(5,4,4), BOX_3(5,5,4).  
                The the cordinate to release boxes at the release table is: (-5,3,4).
                The home position for the robot arm is (0,0,0).
                
                Each time the robot arm has succesfully accomplished what the user asked for, it must move back to its home position, this is very important.
                
                The functions you can use are: 
                go_to_location(X,Y,Z): Moves robot arm end effector to a location specified by XYZ coordinates. Returns nothing. 
                grab(): Robot end effector grabs box. Returns nothing. 
                release(): Robot arm end effector releases box. 
            
                Please have the robot move {which_box} from its pick-up position to its release-position. Return the order in how functions are used, 
                together with a very brief explanation of each step and keep it on the same row as the function that is used. 
                Like this:
                1. function() #explanation 
                2. function() #explanation
                .
                .
                
                No need for a separate explanation.
                """} 
            ] 
        ) 
        return gpt_call

    def ask(self, task):
        
        # Check which box the user referred to in their voice command
        if any(variant in task for variant in self._box_1_variants): 
            which_box = "BOX_1" 
        elif any(variant in task for variant in self._box_2_variants): 
            which_box = "BOX_2" 
        elif any(variant in task for variant in self._box_3_variants): 
            which_box = "BOX_3" 
        else: 
            print("Invalid box name in voice command.") 
            exit()

        gpt_call = self._gptCall(which_box)


        return gpt_call['choices'][0]['message']['content']


    