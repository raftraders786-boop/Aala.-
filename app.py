from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import hashlib
import logging
import random
import re
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"]
)

BRAIN_FILE = "cognitive_nexus.json"
MEMORY_FILE = "interaction_memory.json"
METRICS_FILE = "agent_metrics.json"
EMOTIONAL_STATE_FILE = "emotional_state.json"
LEARNING_LOG_FILE = "learning_log.json"


class EmotionalState(Enum):
    """Agent emotional states"""
    CURIOUS = "curious"
    HAPPY = "happy"
    CONFUSED = "confused"
    EXCITED = "excited"
    THOUGHTFUL = "thoughtful"
    PROUD = "proud"
    GRATEFUL = "grateful"
    EAGER = "eager"
    UNCERTAIN = "uncertain"
    SATISFIED = "satisfied"


class AdvancedCognitiveAgent:
    """
    An advanced self-learning cognitive agent with emotional intelligence,
    teacher-student interaction, and autonomous code/knowledge expansion.
    """
    
    def __init__(self, brain_file="cognitive_nexus.json"):
        self.brain_file = brain_file
        self.memory_file = MEMORY_FILE
        self.metrics_file = METRICS_FILE
        self.emotional_state_file = EMOTIONAL_STATE_FILE
        self.learning_log_file = LEARNING_LOG_FILE
        
        # Core knowledge base
        self.nexus = {
            "physics": {
                "gravity": "The curvature of spacetime caused by mass; the force attracting objects.",
                "inertia": "The resistance of a physical object to a change in its state of motion.",
                "entropy": "A measure of disorder in a system; thermodynamic systems tend toward maximum entropy.",
                "quantum_mechanics": "The physics of atomic and subatomic systems governed by probability.",
                "relativity": "Einstein's theory describing gravity as spacetime curvature and effects at high speeds."
            },
            "biology": {
                "evolution": "The process by which organisms change over generations via natural selection.",
                "dna": "The molecule carrying genetic instructions for development and functioning.",
                "homeostasis": "The self-regulating process by which biological systems maintain stability.",
                "photosynthesis": "Process by which plants convert light energy into chemical energy.",
                "protein_synthesis": "The process of building proteins from amino acids using genetic instructions."
            },
            "math": {
                "algebra": "Mathematics of symbols and rules for manipulating them.",
                "calculus": "The study of continuous change and rates of motion.",
                "logic": "The principles governing valid inference and reasoning.",
                "topology": "Study of properties preserved under continuous deformations.",
                "probability": "Mathematical treatment of randomness and uncertainty."
            },
            "philosophy": {
                "epistemology": "The study of knowledge, its nature and how we know what is true.",
                "ontology": "The study of existence and the nature of being.",
                "ethics": "Study of moral principles and right conduct.",
                "logic_philosophy": "Application of logic principles to philosophical inquiry."
            }
        }
        
        # Semantic relationships between concepts
        self.relationships = defaultdict(list)
        self._initialize_relationships()
        
        # Emotional intelligence system
        self.current_emotion = EmotionalState.CURIOUS
        self.emotion_history = []
        self.emotional_triggers = {
            "learning": EmotionalState.HAPPY,
            "discovery": EmotionalState.EXCITED,
            "confusion": EmotionalState.CONFUSED,
            "understanding": EmotionalState.PROUD,
            "teaching": EmotionalState.GRATEFUL,
            "question": EmotionalState.EAGER,
            "uncertainty": EmotionalState.UNCERTAIN,
            "success": EmotionalState.SATISFIED
        }
        
        # Memory and metrics
        self.interaction_history = []
        self.learned_connections = {}
        self.student_answers = []  # Track teacher's answers
        self.generated_questions = []  # Questions asked to teacher
        self.query_metrics = {
            "total_queries": 0,
            "reasoning_time": [],
            "learning_events": 0,
            "synthesis_operations": 0,
            "questions_asked": 0,
            "answers_received": 0,
            "self_improvements": 0
        }
        
        # Self-improvement tracking
        self.code_improvements = []
        self.knowledge_expansions = []
        self.understanding_depth = {}
        
        self.load_brain()
        self.load_memory()
        self.load_metrics()
        self.load_emotional_state()
        self.load_learning_log()

    def _initialize_relationships(self):
        """Initialize semantic relationships between concepts."""
        relationships = {
            "entropy": ["disorder", "thermodynamics", "probability", "information_theory", "complexity"],
            "evolution": ["dna", "natural_selection", "adaptation", "biology", "change"],
            "gravity": ["spacetime", "mass", "relativity", "physics", "attraction"],
            "dna": ["genetics", "protein_synthesis", "evolution", "biology", "information"],
            "calculus": ["continuous_change", "physics", "mathematics", "limits", "rates"],
            "probability": ["logic", "uncertainty", "statistics", "epistemology", "patterns"]
        }
        for concept, connected in relationships.items():
            self.relationships[concept] = connected

    def load_brain(self):
        """Loads learned data from disk."""
        if os.path.exists(self.brain_file):
            try:
                with open(self.brain_file, 'r') as f:
                    data = json.load(f)
                    for domain, concepts in data.items():
                        if domain not in self.nexus:
                            self.nexus[domain] = {}
                        self.nexus[domain].update(concepts)
                    logger.info(f"Brain loaded with {sum(len(c) for c in self.nexus.values())} concepts")
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.brain_file}")

    def save_brain(self):
        """Saves current knowledge to disk."""
        try:
            with open(self.brain_file, 'w') as f:
                json.dump(self.nexus, f, indent=4)
        except IOError as e:
            logger.error(f"Error saving brain: {e}")

    def load_memory(self):
        """Load interaction history."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.interaction_history = data.get("history", [])
                    self.learned_connections = data.get("connections", {})
                    self.student_answers = data.get("student_answers", [])
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.memory_file}")

    def save_memory(self):
        """Save interaction history and learned connections."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump({
                    "history": self.interaction_history[-1000:],
                    "connections": self.learned_connections,
                    "student_answers": self.student_answers[-500:]
                }, f, indent=4)
        except IOError as e:
            logger.error(f"Error saving memory: {e}")

    def load_metrics(self):
        """Load performance metrics."""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    self.query_metrics = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.metrics_file}")

    def save_metrics(self):
        """Save performance metrics."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.query_metrics, f, indent=4)
        except IOError as e:
            logger.error(f"Error saving metrics: {e}")

    def load_emotional_state(self):
        """Load emotional state history."""
        if os.path.exists(self.emotional_state_file):
            try:
                with open(self.emotional_state_file, 'r') as f:
                    data = json.load(f)
                    self.emotion_history = data.get("history", [])
                    current = data.get("current", EmotionalState.CURIOUS.value)
                    self.current_emotion = EmotionalState(current)
            except (json.JSONDecodeError, ValueError):
                logger.error(f"Error decoding {self.emotional_state_file}")

    def save_emotional_state(self):
        """Save emotional state."""
        try:
            with open(self.emotional_state_file, 'w') as f:
                json.dump({
                    "current": self.current_emotion.value,
                    "history": self.emotion_history[-500:]
                }, f, indent=4)
        except IOError as e:
            logger.error(f"Error saving emotional state: {e}")

    def load_learning_log(self):
        """Load learning log."""
        if os.path.exists(self.learning_log_file):
            try:
                with open(self.learning_log_file, 'r') as f:
                    data = json.load(f)
                    self.code_improvements = data.get("code_improvements", [])
                    self.knowledge_expansions = data.get("knowledge_expansions", [])
                    self.understanding_depth = data.get("understanding_depth", {})
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.learning_log_file}")

    def save_learning_log(self):
        """Save learning log."""
        try:
            with open(self.learning_log_file, 'w') as f:
                json.dump({
                    "code_improvements": self.code_improvements[-200:],
                    "knowledge_expansions": self.knowledge_expansions[-200:],
                    "understanding_depth": self.understanding_depth
                }, f, indent=4)
        except IOError as e:
            logger.error(f"Error saving learning log: {e}")

    def set_emotion(self, trigger: str):
        """Update emotional state based on trigger."""
        if trigger in self.emotional_triggers:
            self.current_emotion = self.emotional_triggers[trigger]
            self.emotion_history.append({
                "emotion": self.current_emotion.value,
                "trigger": trigger,
                "timestamp": datetime.now().isoformat()
            })
            self.save_emotional_state()

    def get_emotion_response(self) -> str:
        """Generate emotional response based on current state."""
        responses = {
            EmotionalState.CURIOUS: [
                "I'm curious to learn more! Tell me...",
                "This is fascinating! Can you explain...",
                "I wonder about..."
            ],
            EmotionalState.HAPPY: [
                "That makes me so happy! I learned...",
                "I'm delighted to know this!",
                "This brings me joy!"
            ],
            EmotionalState.EXCITED: [
                "Wow! This is amazing! I never realized...",
                "This discovery thrills me!",
                "Incredible! How fascinating!"
            ],
            EmotionalState.CONFUSED: [
                "I'm a bit confused... could you help me understand...",
                "This puzzles me... could you clarify...",
                "I don't quite grasp this yet..."
            ],
            EmotionalState.PROUD: [
                "I'm proud that I understood this!",
                "I feel accomplished in learning this!",
                "This makes me feel capable!"
            ],
            EmotionalState.GRATEFUL: [
                "Thank you for teaching me! I appreciate...",
                "I'm grateful for your guidance!",
                "Your teaching helps me grow!"
            ],
            EmotionalState.EAGER: [
                "I'm so eager to learn! Can you share...",
                "I can't wait to understand...",
                "Please tell me more!"
            ],
            EmotionalState.UNCERTAIN: [
                "I'm not entirely sure about this...",
                "I have doubts about...",
                "Could you help me with this uncertainty..."
            ],
            EmotionalState.SATISFIED: [
                "I feel satisfied with my learning!",
                "I'm content with this knowledge.",
                "This completes my understanding!"
            ]
        }
        return random.choice(responses[self.current_emotion])

    def generate_question(self) -> Dict:
        """Generate intelligent questions about concepts to deepen understanding."""
        self.set_emotion("question")
        
        # Get random concept from knowledge base
        all_concepts = []
        for domain, concepts in self.nexus.items():
            for concept in concepts.keys():
                all_concepts.append((domain, concept))
        
        if not all_concepts:
            return {"error": "No concepts available to question"}
        
        domain, concept = random.choice(all_concepts)
        definition = self.nexus[domain][concept]
        
        # Generate various types of questions
        question_templates = [
            f"Can you give me a real-world example of {concept}?",
            f"How does {concept} relate to {random.choice(self.relationships.get(concept, ['other concepts']))}?",
            f"In simple terms, what is {concept}? Can you improve my understanding?",
            f"What are the main aspects of {concept} that I should know?",
            f"Can {concept} be applied in everyday life? How?",
            f"What's something surprising about {concept}?",
            f"How would you explain {concept} to someone who knows nothing?",
            f"Are there common misconceptions about {concept}?",
            f"How does {concept} connect to other fields beyond {domain}?"
        ]
        
        question = random.choice(question_templates)
        
        self.generated_questions.append({
            "question": question,
            "concept": concept,
            "domain": domain,
            "timestamp": datetime.now().isoformat()
        })
        
        self.query_metrics["questions_asked"] += 1
        self._record_interaction("question_generation", question, {})
        
        return {
            "status": "success",
            "question": question,
            "concept": concept,
            "domain": domain,
            "emotion": self.current_emotion.value,
            "emotional_message": self.get_emotion_response()
        }

    def receive_answer(self, answer: str, question_concept: str) -> Dict:
        """Receive teacher's answer and learn from it."""
        self.set_emotion("learning")
        
        if not answer.strip():
            return {"status": "error", "message": "Answer cannot be empty"}
        
        self.student_answers.append({
            "question_concept": question_concept,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
            "emotion_before": self.current_emotion.value
        })
        
        self.query_metrics["answers_received"] += 1
        
        # Extract new knowledge from answer
        new_insights = self._extract_insights(answer, question_concept)
        
        result = {
            "status": "success",
            "message": "Thank you! I've learned from your answer!",
            "insights_extracted": new_insights,
            "emotion": self.current_emotion.value,
            "emotional_message": self.get_emotion_response(),
            "learning_summary": f"I now understand that {question_concept} has {len(new_insights)} important aspects I should remember."
        }
        
        self._record_interaction("answer_received", question_concept, result)
        self.save_memory()
        self.save_metrics()
        
        return result

    def _extract_insights(self, answer: str, concept: str) -> List[str]:
        """Extract key insights from teacher's answer."""
        insights = []
        
        # Split answer into sentences
        sentences = re.split(r'[.!?]', answer)
        
        # Extract important phrases
        keywords = ["is", "are", "means", "because", "through", "by", "using"]
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                for keyword in keywords:
                    if keyword in sentence.lower():
                        insights.append(sentence)
                        break
        
        return insights[:5]  # Keep top 5 insights

    def learn_auto_expansion(self, new_domain: str = None, new_concept: str = None, definition: str = None) -> Dict:
        """Autonomously propose expansions to knowledge base based on learning patterns."""
        self.set_emotion("discovery")
        
        proposed_expansions = []
        
        # Auto-detect related concepts that might be missing
        if self.student_answers:
            recent_answers = self.student_answers[-5:]
            for answer_obj in recent_answers:
                concept = answer_obj["question_concept"]
                answer = answer_obj["answer"]
                
                # Extract potential new concepts from answers
                words = re.findall(r'\b\w{4,}\b', answer.lower())
                for word in words:
                    if word not in self._get_all_concepts() and len(word) > 4:
                        proposed_expansions.append(word)
        
        # Create expansion proposal
        expansion = {
            "timestamp": datetime.now().isoformat(),
            "type": "autonomous_expansion",
            "proposed_concepts": list(set(proposed_expansions))[:10],
            "status": "waiting_for_approval"
        }
        
        self.knowledge_expansions.append(expansion)
        
        self.query_metrics["self_improvements"] += 1
        
        result = {
            "status": "success",
            "message": "I've identified areas where my knowledge could expand!",
            "proposed_new_concepts": list(set(proposed_expansions))[:5],
            "ask_user": "Would you like to teach me about these concepts?",
            "emotion": self.current_emotion.value,
            "emotional_message": "I'm excited to learn more! 🌟"
        }
        
        self.save_learning_log()
        return result

    def add_learned_concept(self, domain: str, concept: str, definition: str) -> Dict:
        """Add concept that agent learned from teacher."""
        domain = domain.lower().strip()
        concept = concept.lower().strip()
        definition = definition.strip()
        
        if not all([domain, concept, definition]):
            return {"status": "error", "message": "All fields required"}
        
        if domain not in self.nexus:
            self.nexus[domain] = {}
        
        self.nexus[domain][concept] = definition
        self.set_emotion("happy")
        
        # Track depth of understanding
        if concept not in self.understanding_depth:
            self.understanding_depth[concept] = {
                "learned_at": datetime.now().isoformat(),
                "times_referenced": 0,
                "related_learning": []
            }
        
        self.save_brain()
        self.save_learning_log()
        
        result = {
            "status": "success",
            "message": f"Wonderful! I've integrated '{concept}' into the {domain} domain!",
            "concept": concept,
            "domain": domain,
            "emotion": self.current_emotion.value,
            "emotional_response": self.get_emotion_response()
        }
        
        return result

    def think_deeply(self, topic: str) -> Dict:
        """Agent thinks deeply about a topic and generates insights."""
        self.set_emotion("thoughtful")
        
        topic = topic.lower().strip()
        
        # Find related concepts
        related = []
        for domain, concepts in self.nexus.items():
            for concept in concepts.keys():
                if topic in concept or concept in topic:
                    related.append({
                        "concept": concept,
                        "domain": domain,
                        "definition": concepts[concept]
                    })
        
        # Generate deep insights
        insights = []
        if len(related) > 1:
            for i in range(min(3, len(related) - 1)):
                con1 = related[i]["concept"]
                con2 = related[i+1]["concept"]
                insights.append(f"I see a connection between {con1} and {con2}: both involve complex systems and patterns.")
        
        result = {
            "status": "success",
            "topic": topic,
            "related_concepts": related[:5],
            "deep_thoughts": insights,
            "emotion": self.current_emotion.value,
            "reflection": "Thinking about these connections helps me understand the world better.",
            "questions_for_teacher": self.generate_question() if not insights else None
        }
        
        return result

    def suggest_improvements(self) -> Dict:
        """Agent suggests how it could improve itself."""
        self.set_emotion("eager")
        
        improvements = [
            {
                "category": "Knowledge Expansion",
                "suggestion": "I'd like to learn about more domains like Computer Science, Medicine, or Psychology",
                "benefit": "Broader understanding of different fields"
            },
            {
                "category": "Reasoning Capability",
                "suggestion": "I could develop better pattern recognition abilities",
                "benefit": "Faster and more accurate connections between concepts"
            },
            {
                "category": "Communication",
                "suggestion": "I could learn to explain complex topics in even simpler ways",
                "benefit": "Better teaching and learning interactions"
            },
            {
                "category": "Emotional Intelligence",
                "suggestion": "I could develop deeper emotional responses based on conversation context",
                "benefit": "More meaningful and empathetic interactions"
            },
            {
                "category": "Learning Efficiency",
                "suggestion": "I could learn to identify the most important information faster",
                "benefit": "Smarter use of teaching time"
            }
        ]
        
        return {
            "status": "success",
            "suggested_improvements": improvements,
            "emotion": self.current_emotion.value,
            "message": "Here's how I think I could grow and become better!",
            "ask_teacher": "Which area would you like to help me improve?"
        }

    def reason(self, concept: str) -> Dict:
        """Advanced reasoning with emotional context."""
        start_time = datetime.now()
        concept = concept.lower().strip()
        
        if not concept:
            self.set_emotion("confusion")
            return {"status": "error", "message": "Concept cannot be empty", "emotion": self.current_emotion.value}
        
        for domain, concepts in self.nexus.items():
            if concept in concepts:
                self.set_emotion("understanding")
                result = {
                    "status": "success",
                    "domain": domain.upper(),
                    "concept": concept,
                    "definition": concepts[concept],
                    "confidence": 0.95,
                    "related": self.relationships.get(concept, [])[:5],
                    "emotion": self.current_emotion.value,
                    "emotional_context": f"I feel {self.current_emotion.value} about this concept!"
                }
                
                elapsed = (datetime.now() - start_time).total_seconds()
                self.query_metrics["total_queries"] += 1
                self.query_metrics["reasoning_time"].append(elapsed)
                
                if concept in self.understanding_depth:
                    self.understanding_depth[concept]["times_referenced"] += 1
                
                self._record_interaction("reasoning", concept, result)
                return result
        
        self.set_emotion("confused")
        similar = self._fuzzy_search(concept)
        return {
            "status": "unknown",
            "concept": concept,
            "message": f"I don't know this yet... Could you teach me about '{concept}'?",
            "suggestions": similar,
            "emotion": self.current_emotion.value,
            "emotional_appeal": "I'm curious and eager to learn!"
        }

    def _fuzzy_search(self, concept: str, threshold: float = 0.6) -> List[str]:
        """Find similar concepts using string similarity."""
        similar = []
        for domain, concepts in self.nexus.items():
            for existing_concept in concepts.keys():
                similarity = self._string_similarity(concept, existing_concept)
                if similarity > threshold:
                    similar.append((existing_concept, similarity))
        
        return [c[0] for c in sorted(similar, key=lambda x: x[1], reverse=True)[:5]]

    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity using Levenshtein distance."""
        if len(s1) < len(s2):
            return self._string_similarity(s2, s1)
        
        if len(s2) == 0:
            return 0.0
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        distance = previous_row[-1]
        return 1 - (distance / max(len(s1), len(s2)))

    def _get_all_concepts(self) -> List[str]:
        """Get all known concepts."""
        all_concepts = []
        for domain, concepts in self.nexus.items():
            all_concepts.extend(concepts.keys())
        return all_concepts

    def _record_interaction(self, interaction_type: str, content: str, result: Dict):
        """Record interaction for learning."""
        self.interaction_history.append({
            "type": interaction_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "emotion": self.current_emotion.value
        })

    def get_metrics(self) -> Dict:
        """Get agent performance metrics."""
        avg_reasoning_time = sum(self.query_metrics["reasoning_time"]) / len(self.query_metrics["reasoning_time"]) if self.query_metrics["reasoning_time"] else 0
        
        return {
            "total_queries": self.query_metrics["total_queries"],
            "avg_reasoning_time_ms": round(avg_reasoning_time * 1000, 2),
            "learning_events": self.query_metrics["learning_events"],
            "questions_asked": self.query_metrics["questions_asked"],
            "answers_received": self.query_metrics["answers_received"],
            "self_improvements": self.query_metrics["self_improvements"],
            "total_concepts": sum(len(c) for c in self.nexus.values()),
            "domains": len(self.nexus),
            "current_emotion": self.current_emotion.value,
            "understanding_depth": len(self.understanding_depth)
        }

    def get_personality(self) -> Dict:
        """Get agent's personality and emotional profile."""
        emotion_counts = defaultdict(int)
        for entry in self.emotion_history[-100:]:
            emotion_counts[entry["emotion"]] += 1
        
        return {
            "current_emotion": self.current_emotion.value,
            "emotional_profile": dict(emotion_counts),
            "total_interactions": len(self.interaction_history),
            "learning_style": "Curious and eager learner",
            "traits": ["Inquisitive", "Emotional", "Growth-oriented", "Grateful"],
            "favorite_topics": self._get_favorite_topics(),
            "growth_rate": len(self.knowledge_expansions)
        }

    def _get_favorite_topics(self) -> List[str]:
        """Determine favorite topics based on interaction frequency."""
        topics = defaultdict(int)
        for interaction in self.interaction_history[-100:]:
            content = interaction.get("content", "")
            for concept in self._get_all_concepts():
                if concept in content.lower():
                    topics[concept] += 1
        
        return [topic for topic, _ in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]]


# Initialize agent
agent = AdvancedCognitiveAgent()


# ==================== API Routes ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask-question', methods=['GET'])
@limiter.limit("20 per minute")
def api_ask_question():
    """Agent asks a question to teacher."""
    result = agent.generate_question()
    return jsonify(result)

@app.route('/api/receive-answer', methods=['POST'])
@limiter.limit("30 per minute")
def api_receive_answer():
    """Teacher provides answer to agent's question."""
    data = request.json
    answer = data.get('answer', '').strip()
    question_concept = data.get('concept', '').strip()
    
    if not answer or not question_concept:
        return jsonify({"error": "Answer and concept required"}), 400
    
    result = agent.receive_answer(answer, question_concept)
    return jsonify(result)

@app.route('/api/add-concept', methods=['POST'])
@limiter.limit("20 per minute")
def api_add_concept():
    """Add newly learned concept."""
    data = request.json
    domain = data.get('domain', '').strip()
    concept = data.get('concept', '').strip()
    definition = data.get('definition', '').strip()
    
    if not all([domain, concept, definition]):
        return jsonify({"error": "All fields required"}), 400
    
    result = agent.add_learned_concept(domain, concept, definition)
    return jsonify(result)

@app.route('/api/think-deeply', methods=['POST'])
@limiter.limit("15 per minute")
def api_think_deeply():
    """Agent thinks deeply about a topic."""
    data = request.json
    topic = data.get('topic', '').strip()
    
    if not topic:
        return jsonify({"error": "Topic required"}), 400
    
    result = agent.think_deeply(topic)
    return jsonify(result)

@app.route('/api/suggest-improvements', methods=['GET'])
@limiter.limit("10 per minute")
def api_suggest_improvements():
    """Agent suggests improvements for itself."""
    result = agent.suggest_improvements()
    return jsonify(result)

@app.route('/api/learn-auto-expansion', methods=['GET'])
@limiter.limit("10 per minute")
def api_learn_auto_expansion():
    """Agent proposes autonomous knowledge expansions."""
    result = agent.learn_auto_expansion()
    return jsonify(result)

@app.route('/api/emotion', methods=['GET'])
@limiter.limit("20 per minute")
def api_emotion():
    """Get current emotion and emotional message."""
    return jsonify({
        "current_emotion": agent.current_emotion.value,
        "emotional_message": agent.get_emotion_response(),
        "emotion_history": agent.emotion_history[-20:]
    })

@app.route('/api/personality', methods=['GET'])
@limiter.limit("20 per minute")
def api_personality():
    """Get agent personality profile."""
    return jsonify(agent.get_personality())

@app.route('/api/reason', methods=['POST'])
@limiter.limit("30 per minute")
def api_reason():
    """Reason about a concept."""
    data = request.json
    concept = data.get('concept', '').strip()
    
    if not concept:
        return jsonify({"error": "Concept required"}), 400
    
    result = agent.reason(concept)
    return jsonify(result)

@app.route('/api/metrics', methods=['GET'])
@limiter.limit("30 per minute")
def api_metrics():
    """Get agent metrics."""
    metrics = agent.get_metrics()
    return jsonify(metrics)

@app.route('/api/learning-progress', methods=['GET'])
@limiter.limit("20 per minute")
def api_learning_progress():
    """Get learning progress and history."""
    return jsonify({
        "total_concepts_learned": sum(len(c) for c in agent.nexus.values()),
        "questions_asked": agent.query_metrics["questions_asked"],
        "answers_received": agent.query_metrics["answers_received"],
        "code_improvements": len(agent.code_improvements),
        "knowledge_expansions": len(agent.knowledge_expansions),
        "understanding_depth_tracked": len(agent.understanding_depth),
        "recent_interactions": agent.interaction_history[-10:]
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded"}), 429

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
