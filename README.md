# AOCO - Automatic Observation and Correction of (subroutine) Operations

AOCO is an automatic code correction and grading tool that works for small to medium complexity ARM subroutines.
It was developed to be used as an automated solution to grade freshmen students' assignments and practical exams and was successfully used for the first time in a [Microprocessor and Personal Computers course](https://sigarra.up.pt/feup/en/UCURR_GERAL.FICHA_UC_VIEW?pv_ocorrencia_id=436431) at the Faculty of Engineering of the University of Porto during the 2nd semester of 2019/2020.
The acronym was inspired from a preceeding course with the same abbreviation where the tool was first tested.

## Installation

The tool is available through a Docker image, therefore that is the only **prerequisite**. Check the [official Docker documentation](https://docs.docker.com/get-docker/) to see how to install it for your operating system.

With Docker available, all you need to do is run `docker pull cyrilico/aoco-code-correction` in a terminal.

## Usage
1. Isolate your input files in a folder anywhere in your filesystem.
2. Start the container, alongside an interactive session, by running `docker run -v /path/to/input/files:/destination/path/on/container -it cyrilico/aoco-code-correction`.
    - The `-v` option allows to easily pass files from and to the container.
    - The destination path on the container can be anywhere really, as long as the tool can write files there. It needs not to exist *a priori*. If in doubt, choose somewhere below the `/home` directory.
3. When inside the container, run the tool with the command `code-correction`. Use the `-h` (help) option for details on each required and optional argument. You can also check the table below.

### Usage Help
`code-correction [-h] -sr SR -t T -sm SM [SM ...] [-gfd GFD] [-ffd FFD] [-grf GRF] [-tout TOUT] [-fpre FPRE]`

| Argument      | Description   | Required?  | Default value
| ------------- |:-------------:| ----------:|-----:|
| -h, --help      | Show usage help message and exit | No | -
| -sr *file.yml*      | YAML file containing subroutines definition      |   Yes | -
| -t *file.yml* | YAML file containing test cases for grading  | Yes | -
| -sm *SM1.zip* [*SM2.zip*, ...] | Whitespace separated list of .zip files corresponding to student submissions (wildcards are also possible, such as *up\*.zip*). | Yes | -
|  -gfd *folder* | Path to folder to store temporary files necessary for grading a submission (e.g., compiled binaries). Recreated & deleted every submission. Needs not to exist *a priori*. | No | 'grading'
|  -ffd *folder* | Folder to store grading feedback for each submission (one file per each). Needs not to exist *a priori*. | No | 'feedback'
|  -grf *file.csv* | CSV file to store final submission grades. | No | 'grades.csv'
| -tout *timeout* | Float timeout value for when running compiled submissions. If a program takes longer, test automatically fails. Expressed in seconds. | No | 2
| -fpre *precision* | Floating point threshold, for when comparing floating point number outputs (test fails if value does not lie within [VALUE-                   threshold,VALUE+threshold]). | No | 1e-6

## Examples
Check the [`examples`](https://github.com/cyrilico/aoco-code-correction/tree/master/examples) folder for possible input and output files feeded to and produced by the tool.

### Inputs
Example YAML configuration files are provided (`examples/input/subroutines.yaml` and `examples/input/tests.yaml`). The subroutines defined there would correspond to the following C functions:
- SOMA: `int SOMA(int p1, int p2)`
- SOMA_V: `int SOMA_V(int* p1, int p2)`
- somaVFSIMDFEX1A: `void somaVFSIMDFEX1A(float* p1, float* p2, int p3, float* result)`
- testmixed: `int testmixed(int* result1, char* result2)`
- teststring: `void teststring(int* non_writable_p1)`

Parameters/Return values and Inputs/Outputs in the YAML file are always lists. Writable arrays are considered both inputs and outputs to the respective subroutine.

Currently, the following data types are supported:
- int
- float
- double
- string/char* (if the first is detected, it is converted to the second)
- array *scalar_type* (e.g., array float for float*, array int for int*) 

These data types lead to a variety of supported subroutine types. This type is automatically determined by the tool, given the output types provided in the YAML configuration:
- numeric (returns a single numeric value, e.g., `int foo(int bar)`)
- array (outputs are writable arrays/strings, e.g., `void sum_arrays(int* arr1, int* arr2, int n, int* result)`)
- mixed (returns a numeric value and has writable arrays passed, e.g., `int count(int* param1, int* writable1, char* writable2)`)
- void (do not return anything or write to eventual array parameters; output is printed directly from assembly code, e.g., `void hello_world_n_times(int n)`)

### Outputs
The program generates one CSV file (e.g., `examples/output/grades.csv`), with the submission grades per subroutine, and a general grade (average of all values), and a feedback file for each submission (e.g. `examples/output/feedback/up222222222.txt`) with information on the number of tests passed and possible unexpected outputs.
Only incorrect test outputs or unexpected errors are verbosed in this file.
Compilation and runtime errors are captured and pasted directly from *stderr*.

## Miscellaneous
- Currently, submission zips are expected to follow a structure that respects a template to more easily incorporate real faculty student submissions, similar to the following:
```
up222222222[irrelevant_text].zip
└───up222222222
   │   subr1.s
   │   subr2.s
   |   ...
   |   subrn.s
```
Failure in complying with this structure may result in unexpected program behavior.

- Subroutine file names are case insensitive (e.g., program accepts subroutine file *sOMa.s* for subroutine SOMA), but subroutine names in declarations must match exactly what provided in the YAML files.
- Not all custom subroutines included in the submission need to be graded, i.e., it is possible to grade an exercise where you give students a file with an implemented subroutine that will be useful in implementing another subroutine which will be graded.
- In subroutines where arrays (pointers) are "returned" (i.e., passed to the function as writable memory), they must be the last subroutine parameters (inputs), otherwise the tool will not identify them as such.
- In void subroutines, the subroutine should not print a newline in the end of the output, as the program already does that automatically (otherwise tests might fail when they shouldn't).

## Contributing
Though there is no official template, as long as they are well explained and add value, Pull Requests are welcome, as there are always ways the tool can be improved. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)