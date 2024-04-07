from wave_file_manager import wave_file_write_samples, wave_file_read_sample
from exclude_silence_process import get_samples_without_silences
import sys
from os import path
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (400,200)

def check_input_file(filename):
    if len(filename) < 5:
        return "Nom du fichier invalide"
    
    input_split = filename.split(".")
    if input_split == 1:
        return "le fichier n'a pas d'extension"
    
    if input_split[-1].lower() != "wav":
        return 'Uniquement les fichiers wav sont supportés'
    
    return None

"""if len(sys.argv)<2:
    print("Vous devez donner un nom de fichier qui existes")
    exit(0)

input_filename = sys.argv[1]
input_filename_error = check_input_file(input_filename)
if input_filename_error:
    print("ERREUR:", input_filename_error)
    exit(0)

print("Fichier d'entrée", input_filename)
# 1- Lecture du fichier wav et recuperation des samples
#input_filename = "test1.wav"
wav_samples = wave_file_read_sample(input_filename)
if wav_samples == None:
    print("ERREUR: Aucun sample a la lecture du fichier wav")
    exit(0)

# 2- Prossessing algo pour supprimer les silence
wav_samples_without_silences = get_samples_without_silences(wav_samples)


# 3- ecriture du fichier wave de sortir 
output_filename = input_filename[:-4] + "_OUT" + input_filename[-4:]
print("OUTPUT FILENAME", output_filename)
wave_file_write_samples(output_filename, wav_samples_without_silences)"""

class SilenceRemoverApp(App):
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.message_label = Label(text="Deposer un fichier Wav")
        return self.message_label
    
    def _on_file_drop(self, window, file_path):
        input_filename = file_path.decode("utf-8")
        self.message_label.text = input_filename
        input_filename_error = check_input_file(input_filename)
        if input_filename_error:
            print("ERREUR:", input_filename_error)
            self.message_label.text = "ERREUR:\n"+ input_filename_error
            return

        wav_samples = wave_file_read_sample(input_filename)
        if wav_samples == None:
            self.message_label.text = "ERREUR:\n  Aucun sample a la lecture du fichier wav"
            return

        # 2- Prossessing algo pour supprimer les silence
        wav_samples_without_silences = get_samples_without_silences(wav_samples)


        # 3- ecriture du fichier wave de sortir 
        output_filename = input_filename[:-4] + "_OUT" + input_filename[-4:]
        print("OUTPUT FILENAME", output_filename)

        filename = path.basename(output_filename)

        self.message_label.text = "FICHIER GéNéRER:\n"+filename
        wave_file_write_samples(output_filename, wav_samples_without_silences)
    
SilenceRemoverApp().run()