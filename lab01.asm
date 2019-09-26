org		0h
		MOV		20h, #1
		MOV		21h, #1
		MOV		22h, #1
		MOV		23h, #1
		MOV		24h, #1

		MOV		25h, #1
		MOV		26h, #2
		MOV		27h, #3
		MOV		28h, #4
		MOV		29h, #5

		MOV		R0,#20h
		MOV		R1,#25h
		MOV		R2,#0h
		MOV		R3,#5h


loop_start:
		MOV		A, @R0
		MOV		B, @R1
		MUL		AB
		ADD		A, R2
		DJNZ	R3, loop_start

wait:
		SJMP	wait