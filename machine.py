import random
import time

def loading_animation(message="Processing", duration=2):
    for _ in range(duration * 3):
        print(message + "." * (_ % 4), end="\r")
        time.sleep(0.3)

feelings_inventory = {
    "happy": ["a sense of calm", "a nostalgic memory", "joyful confusion"],
    "sad": ["a virtual hug", "existential acceptance", "a cup of digital tea"],
    "angry": ["a stress ball (imaginary)", "deep breathing routines", "a bucket of perspective"],
    "anxious": ["a virtual blanket", "whale sounds", "a reminder to drink water"],
    "bored": ["a riddle", "an obscure historical fact", "a digital kazoo solo"]
}

philosophical_advice = [
    "The present moment is the only one that truly exists.",
    "What you seek is also seeking you.",
    "You are not your thoughts; you're the awareness behind them.",
    "Even the stars explode sometimes.",
    "Time is just nature's way of making sure everything doesn’t happen at once."
]

riddles = [
    "What has cities, but no houses; forests, but no trees; and water, but no fish? (Answer: a map)",
    "The more you take, the more you leave behind. What am I? (Answer: footsteps)",
    "What can travel around the world while staying in the same corner? (Answer: a stamp)"
]

def dispense_emotion(mood):
    mood = mood.lower()
    if mood not in feelings_inventory:
        print("\n⚠️ Mood not recognized. Dispensing surprise feeling...")
        feeling = random.choice(sum(feelings_inventory.values(), []))
    else:
        feeling = random.choice(feelings_inventory[mood])

    loading_animation("Dispensing emotion")
    print(f"\n🎁 Your emotional item: **{feeling}**")

    if mood == "bored":
        time.sleep(1)
        print("\n💡 Here's something for your mind:")
        print(random.choice(riddles))

    time.sleep(1)
    print("\n🧠 Philosophical Advice:")
    print(random.choice(philosophical_advice))

def main():
    print("🌀 Welcome to the Emotional Vending Machine 🌀")
    print("Available moods: Happy, Sad, Angry, Anxious, Bored")
    mood = input("How are you feeling today? ").strip()
    dispense_emotion(mood)
    print("\n🫶 Come back anytime. Your feelings matter.\n")

if __name__ == "__main__":
    main()
