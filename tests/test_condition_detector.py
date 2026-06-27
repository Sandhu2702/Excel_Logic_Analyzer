from core.condition_detector import ConditionDetector


def test_extract_operator():
    detector = ConditionDetector([])

    print(detector._extract_operator("A2>=90"))
    print(detector._extract_operator("B2<50"))
    print(detector._extract_operator('C2="Yes"'))


def test_split_conditions():
    detector = ConditionDetector([])

    result = detector._split_conditions('A2>10,B2<20,C2="Yes"')
    print(result)

def test_extract_if():
    detector = ConditionDetector([])

    formula = '=IF(C2>=90,"Excellent","Average")'

    print(detector._extract_if(formula))

def test_extract_and():
    detector = ConditionDetector([])

    formula = '=IF(AND(C2>=90,D2="Yes"),100,0)'

    print(detector._extract_and(formula))

def test_extract_or():
    detector = ConditionDetector([])

    formula = '=IF(OR(C2>=90,D2="Yes"),100,0)'

    print(detector._extract_or(formula))

def test_extract_ifs():
    detector = ConditionDetector([])

    formula = '=IFS(A2>90,"A",A2>80,"B",A2>70,"C",TRUE,"D")'

    print(detector._extract_ifs(formula))

def test_detect():

    formula_data = {
        "Sheet1": [
           {
                "sheet": "Sheet1",
                "cell": "D2",
                "formula": '=IF(C2>=90,"Excellent","Average")',
                "category": "conditional"
            },
            {
                "sheet": "Sheet1",
                "cell": "E2",
                "formula": '=IF(AND(C2>=90,D2="Yes"),100,0)',
                "category": "logical"
            },
            {
                "sheet": "Sheet1",
                "cell": "F2",
                "formula": '=IFS(A2>90,"A",A2>80,"B",TRUE,"C")',
                "category": "conditional"
            }
        ]
    }

    detector = ConditionDetector(formula_data)

    results = detector.detect()

    for result in results:
        print(result)


def test_summary():

    formula_data = {
        "Sheet1": [
            {
                 "sheet": "Sheet1",
                 "cell": "D2",
                 "formula": '=IF(C2>=90,"Excellent","Average")',
                 "category": "conditional",
            },
            {
                 "sheet": "Sheet1",
                 "cell": "E2",
                 "formula": '=IF(AND(C2>=90,D2="Yes"),100,0)',
                 "category": "logical",
            },
            {
                 "sheet": "Sheet1",
                 "cell": "F2",
                 "formula": '=IFS(A2>90,"A",A2>80,"B",TRUE,"C")',
                 "category": "conditional",
            },
        ]
    }

    detector = ConditionDetector(formula_data)

    detector.detect()

    print(detector.summary())

if __name__ == "__main__":
    test_extract_operator()
    test_split_conditions()
    test_extract_if()
    test_extract_and()
    test_extract_or()
    test_extract_ifs()
    test_detect()
    test_summary()