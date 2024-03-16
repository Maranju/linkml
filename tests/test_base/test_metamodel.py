from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE, LOCAL_METAMODEL_YAML_FILE, METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator


@pytest.mark.slow
@pytest.mark.parametrize(
    "generator,extension,serialize_kwargs",
    [
        (MarkdownGenerator, "markdown", {}),
        (OwlSchemaGenerator, ".owl", {}),
        (RDFGenerator, ".ttl", {"context": "file://" + LOCAL_METAMODEL_LDCONTEXT_FILE}),
        (ContextGenerator, ".context.jsonld", {"base": METAMODEL_NAMESPACE}),
        (JSONLDGenerator, ".json", {"base": METAMODEL_NAMESPACE}),
        (PythonGenerator, ".py", {}),
    ],
)
def test_metamodel(generator, extension, serialize_kwargs, temp_dir, snapshot):
    if not extension.startswith("."):
        # is a directory!
        output_dir = Path(extension) / "meta"
        generator(LOCAL_METAMODEL_YAML_FILE, directory=str(temp_dir)).serialize(directory=str(temp_dir))
        assert temp_dir == snapshot(str(output_dir))
    else:
        generated = generator(LOCAL_METAMODEL_YAML_FILE).serialize(**serialize_kwargs)
        output_file = "meta" + extension
        if extension == ".py":
            compile_python(generated, "test")
        assert generated == snapshot(output_file)


@pytest.mark.slow
@pytest.mark.parametrize("format,extension", [("shex", ".shex"), ("json", ".shexj")])
def test_metamodel_shex(format, extension, snapshot):
    output_file = "meta" + extension
    generated = ShExGenerator(LOCAL_METAMODEL_YAML_FILE, format=format).serialize(format=format)
    assert generated == snapshot(output_file)
