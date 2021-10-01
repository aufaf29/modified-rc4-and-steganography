import sys
import algorithms

if __name__ == "__main__":
    audio = algorithms.AudioStego(sys.argv[3])
    audio.encode(sys.argv[1], key=sys.argv[2], output_file_name=sys.argv[4])

    audio2 = algorithms.AudioStego(sys.argv[4])
    print(audio2.decode(sys.argv[2]))
