import sys

def main():
    if "--version" in sys.argv:
        print("Ateno CLI v0.1.3")
        return
    
    print("🚀 Ateno Spatial Design Environment Initialized.")
    print("Use 'ateno --help' for a list of 3D vision commands.")

if __name__ == "__main__":
    main()