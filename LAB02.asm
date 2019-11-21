;define control registers (with address)
XBR2				EQU		0E3h
P1MDIN			EQU		0ADh
P2MDOUT			EQU		09Ch
WDTCN				EQU		0FFh
SFRPAGE			EQU		084h
P1					EQU		090h
P2					EQU		0C8H

;define control words
CONFIG_PAGE		EQU		0Fh
LEGACY_PAGE		EQU		00h

				;turn-off the watch-dog timer
				MOV		WDTCN, #0DEh
				MOV		WDTCN, #0ADh

				;setup port configuration
				MOV		SFRPAGE, #CONFIG_PAGE
				MOV		XBR2, #0C0h
				MOV		P1MDIN, #0FFh
				MOV		P2MDOUT, #0FFh
				MOV		SFRPAGE, #LEGACY_PAGE

				MOV		R0, #0

				;detect button and display

DETECT:	
				MOV		A,	P1
				JZ		DETECT

				MOV		A, #00000001B
Loop_Begin:
				MOV		P2, A
				RR		A
				LCALL	DELAY
				SJMP	Loop_Begin
				
				MOV		R3,	#50
DELAY:	MOV		R1,	#10
DELAY1:	MOV		R2, #249
DELAY2:	DJNZ	R2, DELAY2
				DJNZ	R1, DELAY1
				DJNZ	R3, DELAY
				RET

				END


				end