#!/usr/bin/env python3
"""Test script to verify natural language chat responses"""

from models.chat_model import TerminacionesChatModel

def test_natural_responses():
    print("=" * 80)
    print("Testing Natural Language Chat Responses")
    print("=" * 80)

    # Initialize chat model
    print("\nInitializing chat model...")
    chat_model = TerminacionesChatModel()

    # Test questions
    test_questions = [
        "¿Qué enchape recomiendas para un baño moderno?",
        "¿Qué pintura uso para exteriores?",
        "Necesito un piso para cocina",
        "¿Qué material me sirve para una piscina?",
        "¿Qué enchape uso en una terraza?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {question}")
        print(f"{'='*80}")

        result = chat_model.generate_response(question)

        print(f"\n📌 On Topic: {result['on_topic']}")
        print(f"\n💬 Response:\n{result['response']}")

        if result['materials_suggested']:
            print(f"\n📦 Materials Suggested: {len(result['materials_suggested'])} items")

        print("\n")

if __name__ == "__main__":
    test_natural_responses()
