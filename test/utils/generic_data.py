DEPARTMENTS = [
    {"dcode": "CSC", "dname": "Computer Science"},
    {"dcode": "MGM", "dname": "Business"},
    {"dcode": "AST", "dname": "Astronomy"}
]

COURSES = [
    {
        "cid": 1,
        "dcode": "CSC",
        "cname": "Intro to Databases"
    },
    {
        "cid": 2,
        "dcode": "CSC",
        "cname": "Algorithm Design"
    },
    {
        "cid": 3,
        "dcode": "AST",
        "cname": "Intro to Astronomy"
    },
    {
        "cid": 4,
        "dcode": "MGM",
        "cname": "Expert Marketing"
    },
    {
        "cid": 5,
        "dcode": "AST",
        "cname": "Secondary Astronomy"
    },
    {
        "cid": 6,
        "dcode": "CSC",
        "cname": "Algorithm Design 2"
    },
    {
        "cid": 7,
        "dcode": "AST",
        "cname": "Third Astronomy"
    }
]

PREREQUISITES = [
    {
        "cid": 6,
        "dcode": "CSC",
        "pcid": 2,
        "pdcode": "CSC"
    },
    {
        "cid": 5,
        "dcode": "AST",
        "pcid": 3,
        "pdcode": "AST"
    },
    {
        "cid": 7,
        "dcode": "AST",
        "pcid": 3,
        "pdcode": "AST"
    },
    {
        "cid": 7,
        "dcode": "AST",
        "pcid": 5,
        "pdcode": "AST"
    }
]

INSTRUCTORS = [
    {
        "iid": 1,
        "ilastname": "Thierry",
        "ifirstname": "Sans",
        "idegree": "MsC",
        "dcode": "CSC"
    },
    {
        "iid": 2,
        "ilastname": "Purva",
        "ifirstname": "Gawde",
        "idegree": "PhD",
        "dcode": "CSC"
    },
    {
        "iid": 3,
        "ilastname": "David",
        "ifirstname": "Lee",
        "idegree": "MsC",
        "dcode": "AST"
    },
    {
        "iid": 4,
        "ilastname": "Walter",
        "ifirstname": "Willy",
        "idegree": "BsC",
        "dcode": "MGM"
    },
]

STUDENTS = [
    {
        "sid": 1,
        "slastname": "Tang",
        "sfirstname": "Alvin",
        "sex": "M",
        "age": 22,
        "dcode": "CSC",
        "yearofstudy": 4
    },
    {
        "sid": 2,
        "slastname": "Zhang",
        "sfirstname": "Sonya",
        "sex": "F",
        "age": 19,
        "dcode": "CSC",
        "yearofstudy": 2
    },
    {
        "sid": 3,
        "slastname": "Babu",
        "sfirstname": "Balaji",
        "sex": "M",
        "age": 20,
        "dcode": "CSC",
        "yearofstudy": 1
    },
    {
        "sid": 4,
        "slastname": "Li",
        "sfirstname": "George",
        "sex": "M",
        "age": 22,
        "dcode": "MGM",
        "yearofstudy": 4
    },
    {
        "sid": 5,
        "slastname": "Smith",
        "sfirstname": "Kelly",
        "sex": "F",
        "age": 23,
        "dcode": "AST",
        "yearofstudy": 1
    },
    {
        "sid": 6,
        "slastname": "Smith",
        "sfirstname": "Kelly",
        "sex": "F",
        "age": 18,
        "dcode": "CSC",
        "yearofstudy": 2
    },
    {
        "sid": 7,
        "slastname": "Bourne",
        "sfirstname": "Jason",
        "sex": "M",
        "age": 30,
        "dcode": "AST",
        "yearofstudy": 4
    }
]
