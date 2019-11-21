	org	0h
	;set array A start at 30h and array B start at 90h 
	;and array size is smaller than 60h
	
	MOV 30h,#1h			;
	MOV 31h,#2h			;
	MOV 32h,#3h			;
	MOV	33h,#4h			;
	MOV 34h,#5h			;
	MOV 60h,#1h			;
	MOV 61h,#2h			;
	MOV 62h,#3h			;
	MOV 63h,#4h			;
	MOV 64h,#5h			;

	MOV	R0,#30h			;
	MOV R1,#60h			;
	MOV	R4,#5h			;
	MOV 	A,@R0			;
	MOV 	B,@R1			;
	MUL 	AB				;
	INC 	R0				;
	INC 	R1				;
	MOV 	R3,A			;
	DEC		R4				;
	
loopstart:
	MOV		A,@R0			;
	MOV 	B,@R1			;
	MUL 	AB				;
	INC 	R0				;
	INC 	R1				;
	ADD		A,R3			;
	MOV		R3,A			;
	DJNZ	R4,loopstart	;
	
	MOV		A,R3			;//save the result at A register

ENF: SJMP ENF

	