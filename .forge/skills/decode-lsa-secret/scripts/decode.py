import sys
import binascii

def decode_lsa(hex_string):
    try:
        # Remove any whitespace/newlines
        hex_string = hex_string.strip()
        # Convert hex to bytes
        raw_bytes = binascii.unhexlify(hex_string)
        # Decode as utf-16-le
        decoded = raw_bytes.decode('utf-16-le', errors='replace')
        # Split by null bytes and filter out empty strings
        parts = [p for p in decoded.split('\x00') if p]
        
        print("Decoded Parts:")
        for i, part in enumerate(parts):
            print(f"[{i+1}] {part}")
            
    except Exception as e:
        print(f"Error decoding hex string: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode.py <hex_string>")
        sys.exit(1)
    
    decode_lsa(sys.argv[1])
