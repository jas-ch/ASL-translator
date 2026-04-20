# ASL-translator: American Sign Lanugage Translator

**ASL-translator** is an AI model that helps translating hand signs into alphabets and numbers for bridging communication with handicaps and learning the sign language.   The model reaches 99.9% accuracy and is easy to plug into any SDK or applications for infinite possibilites. The model utilized **ConvNeXt** and could swap from manual checkpointing to **ModelCheckpoint + lightning**. The model is trained with **ASL Alphabet Dataset** from Kaggle, [link text][https://www.kaggle.com/datasets/grassknoted/asl-alphabet]. To run the inferencing, simply put picture files into the folder of asl/asl_alphbet_test and then run python ./classify.py -h for parameters usage. To run inferencing in a live stream mode, import ASL-translator as a module and invoke the function accordingly.  Sample output in output.txt file.


