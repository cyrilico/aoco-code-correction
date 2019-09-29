.text
.global somaVFSIMDFEX1A
.type somaVFSIMDFEX1A,"function"

somaVFSIMDFEX1A:
    LSR W3, W3, #2
CICLO:
    CBZ X3, FIM
	LDR Q0, [X0]
	LDR Q1, [X1]
	FADD V2.4S, V0.4S, V1.4S
	STR Q2, [X2]
	ADD X0, X0, #16
	ADD X1, X1, #16
	ADD X2, X2, #16
	SUB X3, X3, #1
	B CICLO
FIM:


ret
