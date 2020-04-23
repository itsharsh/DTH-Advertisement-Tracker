from Detection import detect_fct
from Detection import detect_nonFCT
from Detection import detect_branding
from Media import generate_clips

if __name__ == "__main__":
    detect_fct.run()
    # detect_nonFCT.run()
    detect_branding.run()
    generate_clips.run()