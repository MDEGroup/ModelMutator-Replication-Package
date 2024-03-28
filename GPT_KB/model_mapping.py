from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EPackage, EClass, EReference, EAttribute, EObject, EEnum, EOrderedSet, EEnumLiteral



def parse_attributes(path):
    rset = ResourceSet()
    ecore_resource = rset.get_resource(URI(path))
    metamodel = ecore_resource.contents[0]

    class_attributes = {}

    def process_e_class(eclass):
        if isinstance(eclass, EClass):
            attributes = [attribute for attribute in eclass.eStructuralFeatures if isinstance(attribute, EAttribute)]
            class_attributes[eclass.name] = attributes

    def process_e_package(package):
        for eclass in package.eClassifiers:
            process_e_class(eclass)
        for subpack in package.eSubpackages:
            process_e_package(subpack)

    # Assuming the root of the metamodel is an EPackage
    if isinstance(metamodel, EPackage):
        process_e_package(metamodel)

    return class_attributes




def parse_metamodel(path):
    rset = ResourceSet()
    ecore_resource = rset.get_resource(URI(path))
    metamodel = ecore_resource.contents[0]
    rset.metamodel_registry[metamodel.nsURI] = metamodel
    e_packages = []
    e_classes = []
    e_references = []
    e_enums = []

    def process_e_package(package):
        e_packages.append(package)
        for eclassifier in package.eClassifiers:
            if isinstance(eclassifier, EClass):
                e_classes.append(eclassifier)
                for eref in eclassifier.eStructuralFeatures:
                    if isinstance(eref, EReference):
                        e_references.append(eref)
            elif isinstance(eclassifier, EEnum):
                e_enums.append(eclassifier)


    # Assuming the root of the metamodel is an EPackage
    if isinstance(metamodel, EPackage):
        process_e_package(metamodel)
        # If the metamodel contains subpackages, process them as well
        for subpack in metamodel.eSubpackages:
            process_e_package(subpack)

    return e_packages, e_classes, e_references, e_enums

def extract_enum_literals_from_eenum(eenum):
    if not isinstance(eenum, EEnum):
        raise ValueError("Provided object is not an EEnum")

    return [literal.name for literal in eenum.eLiterals]


def append_to_xml_tag(xml_string, append_str):
    # Find the position of the last element before '>'
    last_element_pos = xml_string.rfind('>')

    # If '>' is not found or at the end of the string, return the original string
    if last_element_pos == -1 or last_element_pos == len(xml_string) - 1:
        return xml_string

    # Insert the append_str before the last '>'
    return xml_string[:last_element_pos] + append_str + xml_string[last_element_pos:]



def add_schema_location_to_xmi(xmi_file_path, schema_location, out_file):
    with open(out_file, 'w', encoding='utf-8') as res:
        with open(xmi_file_path, 'r', encoding='utf-8') as model_file:
            lines = model_file.readlines()
            for l in lines:
                if 'xmlns:xmi="http://www.omg.org/XMI' in l:
                    res.write(append_to_xml_tag(l,schema_location))
                else:
                    res.write(l)

def gather_classes(element, class_info):
    if isinstance(element, EObject):
        eclass = element.eClass
        class_name = eclass.name
        if class_name not in class_info:
            # Get attribute names for the class
            attributes = [attr.name for attr in eclass.eAttributes if isinstance(attr, EAttribute)]
            class_info[class_name] = attributes
        for child in element.eContents:
            gather_classes(child, class_info)

def parse_xmi_model_and_count(mm_path, xmi_file_path):
        # Initialize the resource set and load the metamodel
        rset = ResourceSet()
        mm_resource = rset.get_resource(URI(mm_path))
        metamodel = mm_resource.contents[0]

        if not isinstance(metamodel, EPackage):
            raise ValueError("The metamodel at the specified path is not an EPackage")

        # Register the metamodel
        rset.metamodel_registry[metamodel.nsURI] = metamodel

        # Initialize collections and counters
        e_packages = []
        e_classes = []
        e_references = []
        e_enums = []
        e_attributes_count = 0  # Initialize attribute counter
        e_references_count = 0  # Initialize reference counter
        e_classes_count = 0  # Initialize reference counter

        def process_e_package(package):
            nonlocal e_attributes_count, e_references_count, e_classes_count
            e_packages.append(package)
            for eclassifier in package.eClassifiers:
                if isinstance(eclassifier, EClass):
                    e_classes.append(eclassifier)
                    e_classes_count += 1
                    for efeature in eclassifier.eStructuralFeatures:
                        if isinstance(efeature, EReference):
                            e_references.append(efeature)
                            e_references_count += 1
                        elif isinstance(efeature, EAttribute):
                            e_attributes_count += 1
                elif isinstance(eclassifier, EEnum):
                    e_enums.append(eclassifier)

        # Process the root package and any subpackages
        if isinstance(metamodel, EPackage):
            process_e_package(metamodel)
            for subpack in metamodel.eSubpackages:
                process_e_package(subpack)

        # Load the model from the specified XMI file path
        model_resource = rset.get_resource(URI(xmi_file_path))
        print(model_resource)

        # Return the model resource along with the attribute and reference counts
        print("mm classes", e_classes_count)
        print("mm attribute", e_attributes_count)
        print("mm_relationship", e_references_count)
        print("tot", e_attributes_count + e_references_count )
        return model_resource

    #tree.write(xmi_file_path, encoding='utf-8', xml_declaration=True)


def xmi_stats(model_resource):
    # Initialize counters for attributes, references, and classes
    attribute_count = 0
    reference_count = 0
    class_count = 0

    # Define a recursive function to traverse the model
    def traverse(obj):
        nonlocal attribute_count, reference_count, class_count
        # Increment class count for each object traversed
        class_count += 1
        for feature in obj.eClass.eAllStructuralFeatures():
            value = obj.eGet(feature)
            if isinstance(feature, EReference):
                if feature.many:
                    reference_count += len(value)
                else:
                    reference_count += 1 if value else 0
            elif isinstance(feature, EAttribute):
                if feature.many:
                    attribute_count += len(value)
                else:
                    attribute_count += 1 if value is not None else 0
            # Recursively traverse referenced objects if the feature is a containment reference
            if isinstance(feature, EReference) and feature.containment:
                if feature.many:
                    for child in value:
                        traverse(child)
                else:
                    if value:
                        traverse(value)

    # Start traversing from the root of the model
    for root in model_resource.contents:
        traverse(root)

    print("model classes:", class_count)
    print("model attributes:", attribute_count)
    print("model references:", reference_count)

    # Calculate the total number of structural features (attributes + references) and classes
    total_elements = attribute_count + reference_count + class_count
    print("total elements in model:", total_elements)

    return class_count, attribute_count, reference_count

if __name__ == '__main__':
    path_rq= 'C:/Users/claud/OneDrive/Desktop/paperTo Submit/Repos/ModelMutator-Replication-Package/EMFCompare/GPTMutators/RQ2/'


    mm_path = path_rq +  "MySQL2KM3/MySQL.ecore"

    #mm_path = "pfsm/PFSM.ecore"
    xmi_path = path_rq + "MySQL2KM3/euro2004-MySQL.model"
    model_resource = parse_xmi_model_and_count(mm_path, xmi_path)
    xmi_stats(model_resource)







