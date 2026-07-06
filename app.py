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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

BRAIN_FILE = "cognitive_nexus.json"
MEMORY_FILE = "interaction_memory.json"
METRICS_FILE = "agent_metrics.json"


class AdvancedCognitiveAgent:
    """
    An advanced multi-domain reasoning system with persistent memory,
    semantic connections, and intelligent synthesis capabilities.
    """
    
    def __init__(self, brain_file="cognitive_nexus.json"):
        self.brain_file = brain_file
        self.memory_file = MEMORY_FILE
        self.metrics_file = METRICS_FILE
        
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
        
        # Memory and metrics
        self.interaction_history = []
        self.learned_connections = {}
        self.query_metrics = {
            "total_queries": 0,
            "reasoning_time": [],
            "learning_events": 0,
            "synthesis_operations": 0
        }
        
        self.load_brain()
        self.load_memory()
        self.load_metrics()

    def _initialize_relationships(self):
        """Initialize semantic relationships between concepts."""
        relationships = {
            "entropy": ["disorder", "thermodynamics", "probability", "information_theory"],
            "evolution": ["dna", "natural_selection", "adaptation", "biology"],
            "gravity": ["spacetime", "mass", "relativity", "physics"],
            "dna": ["genetics", "protein_synthesis", "evolution", "biology"],
            "calculus": ["continuous_change", "physics", "mathematics"],
            "probability": ["logic", "uncertainty", "statistics", "epistemology"]
        }
        for concept, connected in relationships.items():
            self.relationships[concept] = connected

    def load_brain(self):
        """Loads learned data from disk to ensure long-term memory."""
        if os.path.exists(self.brain_file):
            try:
                with open(self.brain_file, 'r') as f:
                    data = json.load(f)
                    for domain, concepts in data.items():
                        if domain not in self.nexus:
                            self.nexus[domain] = {}
                        self.nexus[domain].update(concepts)
                    logger.info(f"Brain loaded from {self.brain_file}")
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.brain_file}")

    def save_brain(self):
        """Saves current knowledge to ensure growth is permanent."""
        try:
            with open(self.brain_file, 'w') as f:
                json.dump(self.nexus, f, indent=4)
            logger.info("Brain saved successfully")
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
                    logger.info("Memory loaded successfully")
            except json.JSONDecodeError:
                logger.error(f"Error decoding {self.memory_file}")

    def save_memory(self):
        """Save interaction history and learned connections."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump({
                    "history": self.interaction_history[-1000:],  # Keep last 1000
                    "connections": self.learned_connections
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

    def reason(self, concept: str) -> Dict:
        """
        Advanced recursive search with path tracking and confidence scoring.
        """
        start_time = datetime.now()
        concept = concept.lower().strip()
        
        if not concept:
            return {"status": "error", "message": "Concept cannot be empty"}
        
        # Direct search
        for domain, concepts in self.nexus.items():
            if concept in concepts:
                result = {
                    "status": "success",
                    "domain": domain.upper(),
                    "concept": concept,
                    "definition": concepts[concept],
                    "confidence": 0.95,
                    "related": self.relationships.get(concept, [])[:5]
                }
                
                # Track metrics
                elapsed = (datetime.now() - start_time).total_seconds()
                self.query_metrics["total_queries"] += 1
                self.query_metrics["reasoning_time"].append(elapsed)
                
                # Record in history
                self._record_interaction("reasoning", concept, result)
                
                return result
        
        # Fuzzy search if not found
        similar = self._fuzzy_search(concept)
        
        return {
            "status": "unknown",
            "concept": concept,
            "message": f"No direct match for '{concept}'. Did you mean: {similar}?",
            "suggestions": similar,
            "confidence": 0.5 if similar else 0.1
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

    def learn(self, domain: str, concept: str, definition: str, confidence: float = 1.0) -> Dict:
        """
        Integrates new knowledge with validation and duplication checking.
        """
        domain = domain.lower().strip()
        concept = concept.lower().strip()
        definition = definition.strip()
        
        if not all([domain, concept, definition]):
            return {"status": "error", "message": "All fields are required"}
        
        if len(definition) < 10:
            return {"status": "error", "message": "Definition must be at least 10 characters"}
        
        # Check for duplicates
        if domain in self.nexus and concept in self.nexus[domain]:
            return {
                "status": "warning",
                "message": f"Concept '{concept}' already exists in {domain}",
                "existing_definition": self.nexus[domain][concept]
            }
        
        if domain not in self.nexus:
            self.nexus[domain] = {}
        
        self.nexus[domain][concept] = definition
        self.query_metrics["learning_events"] += 1
        
        self.save_brain()
        
        result = {
            "status": "success",
            "message": f"Concept '{concept}' integrated into {domain} framework",
            "domain": domain,
            "concept": concept,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        
        self._record_interaction("learning", f"{domain}:{concept}", result)
        self.save_memory()
        self.save_metrics()
        
        return result

    def synthesize(self, concept1: str, concept2: str) -> Dict:
        """
        Advanced synthesis creating semantic bridges between concepts.
        """
        concept1 = concept1.lower().strip()
        concept2 = concept2.lower().strip()
        
        if not concept1 or not concept2:
            return {"status": "error", "message": "Two concepts are required"}
        
        res1 = self.reason(concept1)
        res2 = self.reason(concept2)
        
        # Generate synthesis
        synthesis_key = f"{concept1}_{concept2}"
        
        connection = {
            "concepts": [concept1, concept2],
            "domains": [
                res1.get("domain", "UNKNOWN"),
                res2.get("domain", "UNKNOWN")
            ],
            "analysis": self._generate_synthesis_analysis(res1, res2),
            "created_at": datetime.now().isoformat(),
            "strength": self._calculate_connection_strength(res1, res2)
        }
        
        self.learned_connections[synthesis_key] = connection
        self.query_metrics["synthesis_operations"] += 1
        
        result = {
            "status": "success",
            "concept1": concept1,
            "concept2": concept2,
            "domain1": res1.get("domain"),
            "domain2": res2.get("domain"),
            "definition1": res1.get("definition"),
            "definition2": res2.get("definition"),
            "connection_strength": connection["strength"],
            "synthesis": connection["analysis"],
            "cross_domain_insights": self._find_cross_domain_patterns(concept1, concept2)
        }
        
        self._record_interaction("synthesis", f"{concept1}<->{concept2}", result)
        self.save_memory()
        self.save_metrics()
        
        return result

    def _generate_synthesis_analysis(self, res1: Dict, res2: Dict) -> str:
        """Generate meaningful synthesis between two concepts."""
        domain1 = res1.get("domain", "Unknown")
        domain2 = res2.get("domain", "Unknown")
        
        if domain1 == domain2:
            return f"Both concepts operate within the {domain1} domain, sharing fundamental principles and mathematical frameworks."
        
        analysis_map = {
            ("PHYSICS", "BIOLOGY"): "Concepts bridge physical laws governing matter with biological organization; quantum effects and thermodynamics drive evolution.",
            ("PHYSICS", "MATH"): "Mathematical frameworks describe physical phenomena; calculus models continuous changes in physical systems.",
            ("BIOLOGY", "PHILOSOPHY"): "Biological processes raise questions about consciousness, existence, and the nature of life itself.",
            ("MATH", "PHILOSOPHY"): "Mathematical logic underlies epistemological reasoning and formal systems of thought.",
        }
        
        key = tuple(sorted([domain1, domain2]))
        return analysis_map.get(key, f"These concepts interact at the fundamental level connecting {domain1} and {domain2}.")

    def _calculate_connection_strength(self, res1: Dict, res2: Dict) -> float:
        """Calculate connection strength between concepts."""
        strength = 0.5
        
        if res1.get("status") == "success" and res2.get("status") == "success":
            strength += 0.3
        
        if res1.get("domain") == res2.get("domain"):
            strength += 0.2
        else:
            strength += 0.1
        
        return min(strength, 1.0)

    def _find_cross_domain_patterns(self, concept1: str, concept2: str) -> List[str]:
        """Find patterns connecting concepts across domains."""
        patterns = []
        
        # Common patterns
        pattern_map = {
            "entropy": ["disorder", "complexity", "information"],
            "evolution": ["adaptation", "change", "selection"],
            "gravity": ["attraction", "force", "field"],
        }
        
        for concept in [concept1, concept2]:
            if concept in pattern_map:
                patterns.extend(pattern_map[concept])
        
        return list(set(patterns))[:5]

    def _record_interaction(self, interaction_type: str, content: str, result: Dict):
        """Record interaction for learning and analysis."""
        self.interaction_history.append({
            "type": interaction_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })

    def get_all_knowledge(self) -> Dict:
        """Returns all stored knowledge organized by domain."""
        return self.nexus

    def get_domains(self) -> List[str]:
        """Returns list of all domains."""
        return list(self.nexus.keys())

    def get_concepts_by_domain(self, domain: str) -> Dict:
        """Returns all concepts in a domain."""
        if domain in self.nexus:
            return self.nexus[domain]
        return {}

    def get_concept_count(self) -> Dict:
        """Get count of concepts per domain."""
        return {domain: len(concepts) for domain, concepts in self.nexus.items()}

    def get_interaction_history(self, limit: int = 100, interaction_type: Optional[str] = None) -> List[Dict]:
        """Get recent interaction history."""
        history = self.interaction_history[-limit:]
        if interaction_type:
            history = [h for h in history if h.get("type") == interaction_type]
        return history

    def get_metrics(self) -> Dict:
        """Get agent performance metrics."""
        avg_reasoning_time = sum(self.query_metrics["reasoning_time"]) / len(self.query_metrics["reasoning_time"]) if self.query_metrics["reasoning_time"] else 0
        
        return {
            "total_queries": self.query_metrics["total_queries"],
            "avg_reasoning_time_ms": round(avg_reasoning_time * 1000, 2),
            "learning_events": self.query_metrics["learning_events"],
            "synthesis_operations": self.query_metrics["synthesis_operations"],
            "total_concepts": sum(len(c) for c in self.nexus.values()),
            "domains": len(self.nexus),
            "learned_connections": len(self.learned_connections)
        }

    def search_concepts(self, query: str) -> Dict:
        """Search across all domains for matching concepts."""
        query = query.lower().strip()
        results = {"exact": [], "partial": [], "fuzzy": []}
        
        for domain, concepts in self.nexus.items():
            for concept, definition in concepts.items():
                if concept == query:
                    results["exact"].append({"domain": domain, "concept": concept, "definition": definition})
                elif query in concept or query in definition.lower():
                    results["partial"].append({"domain": domain, "concept": concept, "definition": definition[:100] + "..."})
        
        if not results["exact"] and not results["partial"]:
            results["fuzzy"] = [{"concept": c} for c in self._fuzzy_search(query)]
        
        return results


# Initialize agent
agent = AdvancedCognitiveAgent()


# ==================== API Routes ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reason', methods=['POST'])
@limiter.limit("30 per minute")
def api_reason():
    data = request.json
    concept = data.get('concept', '').strip()
    
    if not concept:
        return jsonify({"error": "Concept is required"}), 400
    
    result = agent.reason(concept)
    return jsonify(result)

@app.route('/api/learn', methods=['POST'])
@limiter.limit("10 per minute")
def api_learn():
    data = request.json
    domain = data.get('domain', '').strip()
    concept = data.get('concept', '').strip()
    definition = data.get('definition', '').strip()
    confidence = data.get('confidence', 1.0)
    
    if not all([domain, concept, definition]):
        return jsonify({"error": "Domain, concept, and definition are required"}), 400
    
    result = agent.learn(domain, concept, definition, confidence)
    return jsonify(result)

@app.route('/api/synthesize', methods=['POST'])
@limiter.limit("20 per minute")
def api_synthesize():
    data = request.json
    concept1 = data.get('concept1', '').strip()
    concept2 = data.get('concept2', '').strip()
    
    if not all([concept1, concept2]):
        return jsonify({"error": "Two concepts are required"}), 400
    
    result = agent.synthesize(concept1, concept2)
    return jsonify(result)

@app.route('/api/knowledge', methods=['GET'])
@limiter.limit("30 per minute")
def api_knowledge():
    return jsonify(agent.get_all_knowledge())

@app.route('/api/domains', methods=['GET'])
@limiter.limit("30 per minute")
def api_domains():
    return jsonify({
        "domains": agent.get_domains(),
        "count": agent.get_concept_count()
    })

@app.route('/api/domain/<domain>', methods=['GET'])
@limiter.limit("30 per minute")
def api_get_domain(domain):
    domain = domain.lower()
    concepts = agent.get_concepts_by_domain(domain)
    
    if not concepts:
        return jsonify({"error": f"Domain '{domain}' not found"}), 404
    
    return jsonify({
        "domain": domain,
        "concepts": concepts,
        "count": len(concepts)
    })

@app.route('/api/search', methods=['POST'])
@limiter.limit("30 per minute")
def api_search():
    data = request.json
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = agent.search_concepts(query)
    return jsonify(results)

@app.route('/api/history', methods=['GET'])
@limiter.limit("20 per minute")
def api_history():
    limit = request.args.get('limit', 50, type=int)
    interaction_type = request.args.get('type', None)
    
    history = agent.get_interaction_history(limit, interaction_type)
    return jsonify({"history": history})

@app.route('/api/metrics', methods=['GET'])
@limiter.limit("30 per minute")
def api_metrics():
    metrics = agent.get_metrics()
    return jsonify(metrics)

@app.route('/api/connections', methods=['GET'])
@limiter.limit("20 per minute")
def api_connections():
    connections = agent.learned_connections
    return jsonify({
        "total_connections": len(connections),
        "connections": dict(list(connections.items())[:50])  # Return first 50
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
