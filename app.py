from flask import Flask, render_template, request
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
import owlrl
app = Flask(__name__)

BASE = Namespace("http://example.org/akademik#")
ONTOLOGY_PATH = "data/academic_ontology_v1.owl"

g = Graph()
g.parse(ONTOLOGY_PATH)

def clean_value(value):
    text = str(value)
    if "#" in text:
        return text.split("#")[-1]
    if "/" in text:
        return text.rstrip("/").split("/")[-1]
    return text

def load_graph():
    graph = Graph()
    graph.parse(ONTOLOGY_PATH)
    return graph

def load_inferred_graph():
    # Load and run reasoner
    graph = load_graph()
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)
    return graph

@app.route("/")
def index():
    graph = load_graph()
    lecturers = sorted({clean_value(s) for s in graph.subjects(RDF.type, BASE.Dosen)})
    courses = sorted({clean_value(s) for s in graph.subjects(RDF.type, BASE.MataKuliah)})
    semesters = sorted({clean_value(o) for o in graph.objects(None, BASE.ditawarkanPadaSemester)})
    return render_template(
        "index.html",
        lecturers=lecturers,
        courses=courses,
        semesters=semesters,
        ontology_path=ONTOLOGY_PATH,
    )

@app.route("/lecturer")
def by_lecturer():
    lecturer = request.args.get("name", "").strip()
    graph = load_graph()
    query = f'''
    PREFIX ex: <http://example.org/akademik#>
    SELECT ?course WHERE {{
        ex:{lecturer} ex:mengampu ?course .
    }}
    ORDER BY ?course
    '''
    results = [clean_value(row.course) for row in graph.query(query)] if lecturer else []
    return render_template(
        "result.html",
        title=f"Mata kuliah yang diajar {lecturer}",
        items=results,
        query=query.strip()
    )

@app.route("/prerequisite")
def prerequisite():
    course = request.args.get("name", "").strip()
    graph = load_graph()
    query = f'''
    PREFIX ex: <http://example.org/akademik#>
    SELECT ?pre WHERE {{
        ex:{course} ex:memilikiPrasyarat ?pre .
    }}
    ORDER BY ?pre
    '''
    results = [clean_value(row.pre) for row in graph.query(query)] if course else []
    return render_template(
        "result.html",
        title=f"Prasyarat untuk {course}",
        items=results,
        query=query.strip()
    )

@app.route("/inferred_prerequisite")
def inferred_prerequisite():
    course = request.args.get("name", "").strip()
    graph = load_inferred_graph()
    query = f'''
    PREFIX ex: <http://example.org/akademik#>
    SELECT DISTINCT ?pre WHERE {{
        ex:{course} ex:memilikiPrasyarat ?pre .
    }}
    ORDER BY ?pre
    '''
    # The reasoner expands the graph to include transitive relations
    results = [clean_value(row.pre) for row in graph.query(query)] if course else []
    
    # We remove the course itself from results because 'Transitive' might occasionally infer self in some logic configurations,
    # though usually not an issue unless it's reflexive. But to be safe:
    results = [r for r in results if r != course]

    return render_template(
        "result.html",
        title=f"Prasyarat (Langsung & Tidak Langsung) untuk {course}",
        items=results,
        query=query.strip()
    )

@app.route("/semester")
def by_semester():
    semester = request.args.get("name", "").strip()
    graph = load_graph()
    query = f'''
    PREFIX ex: <http://example.org/akademik#>
    SELECT ?course WHERE {{
        ?course ex:ditawarkanPadaSemester ex:{semester} .
    }}
    ORDER BY ?course
    '''
    results = [clean_value(row.course) for row in graph.query(query)] if semester else []
    return render_template(
        "result.html",
        title=f"Mata kuliah pada {semester}",
        items=results,
        query=query.strip()
    )

if __name__ == "__main__":
    app.run(debug=True)