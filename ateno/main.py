import sys
import os
import argparse
from . import Ateno

def main():
    parser = argparse.ArgumentParser(description="Ateno Spatial Design CLI")
    parser.add_argument("--version", action="version", version="Ateno CLI v0.1.3")
    parser.add_argument("--api-key", help="Your Ateno API Key (or set ATENO_API_KEY env var)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_2d = subparsers.add_parser("generate-2d", help="Generate a 2D room design")
    parser_2d.add_argument("--image", required=True, help="Path to local image or URL")
    parser_2d.add_argument("--room-type", help="Type of room (e.g., living_room)")
    parser_2d.add_argument("--design", help="Design style (e.g., modern)")

    parser_3d = subparsers.add_parser("generate-3d", help="Generate a 3D spatial design")
    parser_3d.add_argument("--image", required=True, help="Path to local image or URL")
    parser_3d.add_argument("--scene-name", help="Name of the scene")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    api_key = args.api_key or os.environ.get("ATENO_API_KEY")
    if not api_key:
        print("Error: API key is required. Pass --api-key or set ATENO_API_KEY environment variable.")
        sys.exit(1)

    ateno = Ateno(api_key=api_key)

    def print_progress(msg):
        print(f"-> {msg}")

    try:
        if args.command == "generate-2d":
            print("🚀 Starting 2D Generation...")
            payload = {"image": args.image}
            if args.room_type: payload["roomType"] = args.room_type
            if args.design: payload["design"] = args.design
            
            result = ateno.rooms.generate_room_2d(payload, on_progress=print_progress)
            
            print("\n✅ Success!")
            print(f"🎨 Design ID: {result.get('designId')}")
            print(f"🖼️  Image URL: {result.get('generatedImage')}")

        elif args.command == "generate-3d":
            print("🚀 Starting 3D Generation...")
            payload = {"imageBase64": args.image}
            if args.scene_name: payload["sceneName"] = args.scene_name
            
            result = ateno.rooms.generate_room_3d(payload, on_progress=print_progress)
            
            print("\n✅ Success!")
            print(f"📦 Design ID: {result.get('designId')}")
            print(f"🌐 3D Model URL: {result.get('storageUrl')}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()