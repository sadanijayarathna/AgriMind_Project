import sys
import os
import json
import time

# Append the project path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try importing the expert system
try:
    from agrimind_expert_system import AgriMindExpertSystem
except ImportError:
    print("Error: agrimind_expert_system.py not found in the path.")
    sys.exit(1)

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title.upper()} ".center(60, "#"))
    print("=" * 60)

def main_menu():
    expert_system = AgriMindExpertSystem("chemical_rules.json")
    
    while True:
        print_header("AgriMind Unified Advisory System Console")
        print(" 1. Simulate Vision AI Crop Diagnosis (Objective 1)")
        print(" 2. Run Fertilizer Price Forecasting (Objective 2)")
        print(" 3. Validate Tank Chemical Mixtures (Objective 4)")
        print(" 4. Execute End-to-End Integrated Advisory Flow")
        print(" 5. Exit Console")
        print("=" * 60)
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            simulate_crop_diagnosis()
        elif choice == '2':
            run_price_forecasting()
        elif choice == '3':
            validate_mixtures_menu(expert_system)
        elif choice == '4':
            run_integrated_advisory_flow(expert_system)
        elif choice == '5':
            print("\nExiting AgriMind console. Stay safe!")
            break
        else:
            print("\n[!] Invalid selection. Please enter a number between 1 and 5.")
            time.sleep(1)

def simulate_crop_diagnosis():
    print_header("Objective 1: Vision AI Crop Diagnosis")
    print("Select a simulated leaf image to submit to the CNN:")
    print(" 1. tomato_leaf_early_blight.jpg")
    print(" 2. tomato_leaf_late_blight.jpg")
    print(" 3. tomato_leaf_healthy.jpg")
    print(" 4. Cancel")
    
    img_choice = input("Choose image (1-4): ").strip()
    if img_choice == '1':
        print("\n[Vision AI] Loading CNN model local weights...")
        time.sleep(1)
        print("[Vision AI] Preprocessing image (226x226)...")
        time.sleep(0.8)
        print("[Vision AI] Result: Tomato Early Blight (Confidence: 94.2%)")
        print("Recommended Treatment: Apply Chlorothalonil fungicide and Urea fertilizer to recover.")
    elif img_choice == '2':
        print("\n[Vision AI] Loading CNN model local weights...")
        time.sleep(1)
        print("[Vision AI] Result: Tomato Late Blight (Confidence: 97.8%)")
        print("Recommended Treatment: Apply Bordeaux Mixture fungicide and Urea fertilizer to recover.")
    elif img_choice == '3':
        print("\n[Vision AI] Loading CNN model local weights...")
        time.sleep(1)
        print("[Vision AI] Result: Healthy Leaf (Confidence: 99.1%)")
        print("No treatment required.")
    else:
        print("\nDiagnosis cancelled.")
    
    input("\nPress Enter to return to main menu...")

def run_price_forecasting():
    print_header("Objective 2: Fertilizer Price Forecasting")
    print("Evaluating trained sequential forecasting models (SimpleRNN, LSTM, GRU)...")
    time.sleep(1.2)
    
    # Pre-calculated model validation performance metrics on the test set
    print("\nModel Testing Performance Comparison:")
    print("-" * 65)
    print(f"{'Model Name':<15} | {'MAE (USD/ton)':<15} | {'RMSE (USD/ton)':<15} | {'R2 Score':<10}")
    print("-" * 65)
    print(f"{'SimpleRNN':<15} | {'$36.21':<15} | {'$43.12':<15} | {'0.812':<10}")
    print(f"{'LSTM':<15} | {'$22.84':<15} | {'$29.40':<15} | {'0.895':<10}")
    print(f"{'GRU (Winner)':<15} | {'$18.52':<15} | {'$23.97':<15} | {'0.923':<10}")
    print("-" * 65)
    
    print("\n[Advisory Forecast Output]:")
    print("Based on the winning GRU model, the price of Urea is forecasted to DROP by $25/ton next month.")
    print(">> Recommendation: WAIT to purchase bulk quantities of Urea to optimize your budget.")
    input("\nPress Enter to return to main menu...")

def validate_mixtures_menu(expert_system):
    print_header("Objective 4: Tank Mixture Rule Validation")
    print("Available chemicals in database:")
    chems = expert_system.list_chemicals()
    for idx, chem in enumerate(chems, 1):
        print(f" {idx:2d}. {chem['name']} ({chem['category']})")
    
    print("\nEnter a comma-separated list of chemicals you want to mix in your sprayer tank:")
    print("Example: Calcium Nitrate, Magnesium Sulfate")
    
    user_input = input("Mixture: ").strip()
    if not user_input:
        return
        
    mix = [item.strip() for item in user_input.split(',')]
    
    print("\nRunning rule compatibility check...")
    time.sleep(0.8)
    
    report = expert_system.validate_mixture(mix)
    
    print("\n" + "-" * 50)
    print(f"STATUS: {report['status']}")
    print(f"SUMMARY: {report['summary']}")
    print("-" * 50)
    
    if report['conflicts']:
        print("HAZARDS FOUND:")
        for idx, conflict in enumerate(report['conflicts'], 1):
            print(f" {idx}. Pair: {conflict['chemical_1']} + {conflict['chemical_2']}")
            print(f"    Hazard Type: {conflict['type']} ({conflict['severity']})")
            print(f"    Reason: {conflict['reason']}")
            print(f"    Alternative: {conflict['alternative']}")
            
    input("\nPress Enter to return to main menu...")

def run_integrated_advisory_flow(expert_system):
    print_header("Integrated Advisory Simulation Loop")
    print("[SYSTEM] Phase 1: vision leaf diagnostics trigger...")
    time.sleep(1)
    print("[SYSTEM] Simulated Leaf Image submitted: 'tomato_leaf_late_blight.jpg'")
    print("[VISION AI] Diagnosis: **Tomato Late Blight** (98% Confidence)")
    print(">> Prescribed Treatment: Bordeaux Mixture (Fungicide) & Urea (Nutrient Support)")
    print("-" * 60)
    
    print("\n[SYSTEM] Phase 2: running time-series forecaster on prescribed Urea...")
    time.sleep(1.2)
    print("[FORECASTER] Current Urea price: $592.00 / short ton")
    print("[FORECASTER] GRU Model Forecasted Price (Next Month): $567.00 / short ton")
    print(">> Price Advisory: Price is falling. Delay purchase by 30 days to save $25.00/ton.")
    print("-" * 60)
    
    print("\n[SYSTEM] Phase 4: checking chemical tank safety guard rules...")
    time.sleep(1)
    print("The farmer proposes mixing 'Bordeaux Mixture' + 'Urea' + 'Chlorpyrifos' (insecticide for beetles).")
    
    mix = ["Bordeaux Mixture", "Urea", "Chlorpyrifos"]
    report = expert_system.validate_mixture(mix)
    
    print(f"\n[EXPERT SYSTEM] Status: {report['status']}")
    print(f"[EXPERT SYSTEM] Output: {report['summary']}")
    print("\nDetailed Safety Vetoes:")
    for idx, conflict in enumerate(report['conflicts'], 1):
        print(f"  Conflict {idx}: {conflict['chemical_1']} + {conflict['chemical_2']}")
        print(f"  Hazard: {conflict['type']} ({conflict['severity']})")
        print(f"  Description: {conflict['reason']}")
        print(f"  Resolution Advice: {conflict['alternative']}")
    
    print("=" * 60)
    print("SIMULATION ENDED")
    input("\nPress Enter to return to main menu...")

if __name__ == '__main__':
    main_menu()
