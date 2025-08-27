import openai
import base64
import json
import os
from PIL import Image
import requests

def setup_openai(api_key):
    """Setup OpenAI API with your API key"""
    openai.api_key = api_key
    return openai

def encode_image_to_base64(image_path):
    """Convert image to base64 encoding for API"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {str(e)}")
        return None

def analyze_single_image_floor_color(api_key, image_path):
    """Analyze floor color in a single image using OpenAI GPT-4 Vision"""
    try:
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            return "Error: Could not encode image"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze the floor/flooring visible in this image. Focus specifically on the floor surface and provide detailed color information.

Please provide your analysis in this JSON format:
{
    "floor_detected": true/false,
    "floor_material": "wood/tile/carpet/concrete/vinyl/other",
    "primary_color": "main color name (e.g., light brown, beige, oak)",
    "color_tone": "light/medium/dark",
    "color_temperature": "warm/cool/neutral",
    "detailed_description": "detailed description of floor appearance and colors",
    "hex_estimate": "#approximate hex color",
    "rgb_estimate": [R, G, B values],
    "wood_type": "if wood, specify type like oak, maple, etc.",
    "pattern": "solid/striped/patterned/textured"
}

Focus only on the floor. Ignore walls, furniture, and other objects."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0]['message']['content']
        else:
            return f"Error: {response_data.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def compare_floor_colors_openai(api_key, image_path1, image_path2):
    """Compare floor colors between two images using OpenAI GPT-4 Vision"""
    try:
        base64_image1 = encode_image_to_base64(image_path1)
        base64_image2 = encode_image_to_base64(image_path2)
        
        if not base64_image1 or not base64_image2:
            return "Error: Could not encode one or both images"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """I'm showing you two images. Please analyze and compare ONLY the floor/flooring colors in both images.

For each image, identify the floor color, material, and tone. Then compare them and tell me if they match.

Provide your analysis in this JSON format:
{
    "image1_analysis": {
        "floor_color": "primary color name",
        "material": "floor material type",
        "tone": "light/medium/dark",
        "description": "brief color description"
    },
    "image2_analysis": {
        "floor_color": "primary color name", 
        "material": "floor material type",
        "tone": "light/medium/dark",
        "description": "brief color description"
    },
    "comparison": {
        "colors_match": true/false,
        "similarity_percentage": 0-100,
        "final_answer": "YES - colors match" or "NO - colors don't match",
        "explanation": "detailed explanation of why they match or don't match"
    }
}

Focus ONLY on floor colors. Ignore all other elements."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image1}"
                            }
                        },
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image2}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 600
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()
        
        if 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0]['message']['content']
        else:
            return f"Error: {response_data.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error comparing images: {str(e)}"

def extract_json_response(response_text):
    """Extract JSON from OpenAI response"""
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            return None
    except json.JSONDecodeError:
        return None

def main():
    """Main function to compare floor colors using OpenAI"""
    
    print("🤖 OPENAI GPT-4 VISION FLOOR COLOR COMPARISON")
    print("=" * 55)
    
    api_key = input("Enter your OpenAI API key: ").strip()
    if not api_key:
        print("❌ OpenAI API key is required!")
        return
    
    image1_path = input("Enter path to first image: ").strip()
    image2_path = input("Enter path to second image: ").strip()
    
    if not os.path.exists(image1_path):
        print(f"❌ Image 1 not found: {image1_path}")
        return
        
    if not os.path.exists(image2_path):
        print(f"❌ Image 2 not found: {image2_path}")
        return
    
    print(f"\n🔍 Analyzing floor colors...")
    print(f"📸 Image 1: {image1_path}")
    print(f"📸 Image 2: {image2_path}")
    print("-" * 50)
    
    print("🆚 Comparing floor colors with OpenAI GPT-4 Vision...")
    comparison_result = compare_floor_colors_openai(api_key, image1_path, image2_path)
    
    print("\n📊 RAW RESPONSE:")
    print(comparison_result)
    
    json_data = extract_json_response(comparison_result)
    
    if json_data and 'comparison' in json_data:
        print("\n🎯 STRUCTURED RESULTS:")
        print("-" * 30)
        
        if 'image1_analysis' in json_data:
            img1 = json_data['image1_analysis']
            print(f"📸 Image 1 Floor:")
            print(f"   Color: {img1.get('floor_color', 'N/A')}")
            print(f"   Material: {img1.get('material', 'N/A')}")
            print(f"   Tone: {img1.get('tone', 'N/A')}")
        
        if 'image2_analysis' in json_data:
            img2 = json_data['image2_analysis']
            print(f"\n📸 Image 2 Floor:")
            print(f"   Color: {img2.get('floor_color', 'N/A')}")
            print(f"   Material: {img2.get('material', 'N/A')}")
            print(f"   Tone: {img2.get('tone', 'N/A')}")
        
        comparison = json_data['comparison']
        colors_match = comparison.get('colors_match', False)
        similarity = comparison.get('similarity_percentage', 0)
        final_answer = comparison.get('final_answer', 'Unknown')
        explanation = comparison.get('explanation', 'No explanation provided')
        
        print(f"\n🎯 FINAL ANSWER:")
        print(f"{'✅' if colors_match else '❌'} {final_answer}")
        print(f"📊 Similarity: {similarity}%")
        print(f"💬 Explanation: {explanation}")
        
    else:
        print("\n⚠️  Could not extract structured data, but analysis is above.")
    
    return comparison_result

def quick_floor_compare(api_key, image1_path, image2_path):
    """Quick function for simple floor color comparison"""
    try:
        result = compare_floor_colors_openai(api_key, image1_path, image2_path)
        
        # Extract simple answer
        if "YES" in result.upper():
            return "✅ YES - Floor colors match"
        elif "NO" in result.upper():
            return "❌ NO - Floor colors don't match"
        else:
            return result
            
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    main()
