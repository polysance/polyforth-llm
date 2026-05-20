( Ideal in Forth)

( 4821 LIST)
( This is the "minimalist" version for x86, with no "hooks" for future unknown complications. Will make conventions that should survive into more complex versions, but this one will be a "floor" especially in its native chip version. Each sort of "thing" will have a numeric handle starting at 1. The zero handle will mean "null" or undefined. BOREDOMLEVEL is bias between self-satisfaction & disengagement.)

( IDEAL Simplified) EMPTY

( Database) 1 FH 2 FH THRU ( Exist) 3 FH 5 FH THRU

2 BOREDOMLEVEL !
: .EXP "EXP TYPE ; : .RES "RES TYPE ;
: .INT ( i) INTS U@ 256 /MOD SWAP .EXP ." ->" .RES SPACE ;
: .MOOD ( i) "MOOD TYPE ;

: RUN E1 PREVEXP ! 20 0 DO STEP CR I . ." : "
    CURINT @ DUP . .INT #SATIS ?
    EXPECTED @ .RES SPACE MOOD @ .MOOD LOOP ;

( 4822 LIST)
( Experiences, Results, moods are simple, named abstract things. They correspond to processes or events in the Existence du jour, as well as to additional pertinent attributes. The number and attributes of these are small and Existence-dependent, so we denote them internally with small ordinals and define only the "null" value here. Attributes such as names apply to compile-time and to running on "big" computers. M prefix is maximum. # prefix is number of. " is display name. :ID adds an abstract thing and gives it a programmatic name. !SARRAY sets display name for the given ordinal and its class.)

( Static, abstract things)
: :ID ( a lim _id - i) OVER @ = ABORT" Too many!"
DUP @ DUP CONSTANT SWAP TALLY ;
: !SARRAY ( i a _ - i) SWAP 4* + HERE SWAP ! 32 STRING ;

10 CONSTANT MEXP    10 CONSTANT MRES    6 CONSTANT MMOOD
   VARIABLE #EXP       VARIABLE #RES      VARIABLE #MOOD
MEXP SARRAY "EXP    MRES SARRAY "RES    MMOOD SARRAY "MOOD

: :EXP ( _id _dsp - i) #EXP MEXP :ID DUP [’] "EXP !SARRAY ;
: :RES ( same) #RES MRES :ID DUP [’] "RES !SARRAY ;
: :MOOD ( sam) #MOOD MMOOD :ID DUP [’] "MOOD !SARRAY ;

:EXP E0 Null DROP   :RES R0 Null DROP   :MOOD MNOTH Nothing DROP

( 4823 LIST)
( Simple interactions are indexed by an experiment and a result, unique in that combination. All are created dynamically by the environment. Changes in algorithm may add attributes or change storage or indexing methods. Handle is ordinal, which simply denotes order of creation. Ordinal 0 is null. INTS is index; index values res|exp bytes in a halfcell. ?E-R returns nonzero ordinal if the index value exists, index value under false if not. ?INT same but takes experiment & result ordinals. : +INT finds existing or creates new interaction.)

 ( Simple Interactions)
MEXP DUP * CONSTANT MINT VARIABLE #INT 1 #INT !
MINT HARRAY INTS

: ?E-R ( nE-R - iI | nE-R 0) #INT @ 1- FOR
    DUP I INTS U@ = IF DROP R> EXIT THEN NEXT 0 ;
: ?INT ( iE iR - iI | nE-R 0) >< + ?E-R ;
: +INT ( iE iR - iI) ?INT ?DUP 0= IF
    #INT @ DUP MINT = ABORT" Too many prim interactions!"
    SWAP OVER INTS H! #INT TALLY THEN ;

( 4824 LIST)
( Static abstract things are declared at compilation time. PREVEXP is index of experiment made just before the current. CUREXP is index of experiment being made by current cycle. MOOD is an abstract state influencing decision making. #SATIS is self-satisfaction counter BOREDOMLEVEL is bias between self-satisfaction & disengagement. EXPECTED result from current experiment - may be null RESULT actual result from current experiment CURINT interaction for current experiment)

( Existence Simplified)
:EXP E1 E1 DROP :RES R1 R1 DROP
:EXP E2 E2 DROP :RES R2 R2 DROP

:MOOD SATIS SelfSatisfied DROP  :MOOD FRUST Frustrated DROP
:MOOD BORED Bored DROP          :MOOD PAIN Pained DROP
:MOOD PLEAS Pleased DROP

( State variables)
VARIABLE PREVEXP    VARIABLE CUREXP
VARIABLE MOOD       VARIABLE #SATIS     VARIABLE BOREDOMLEVEL

VARIABLE EXPECTED   VARIABLE RESULT     VARIABLE CURINT

( 4825 LIST)
( PREDICT finds the newest interaction employing the given experiment highest ordinal returning handle for its result. If no such interaction exists, returns null result. Because the result of each experiment is always the same, this is appearances only. ENACT performs experiment CUREXP. E1->R1, E2->R2. OTHEREXP finds the experiment with *highest* ordinal differing from the one given. The prototype given returned the *LOWEST* ordinal, but no obvious reason why this would be preferable to the highest. Second version uses highest instead because that covers the case of defaulting to null when there’s no other experiment than the one being enacted.)

( Benefit of Experience)
: PREDICT ( exp - res) #INT @ 1- FOR DUP I INTS C@ = IF
    DROP R> INTS 1+ C@ EXIT THEN NEXT DROP 0 ;

: ENACT ( - res) CUREXP @ E1 = IF R1 ELSE R2 THEN ;

: OTHEREXP ( cur - new) #EXP @ 1 DO DUP I - IF
    DROP 2R> NIP EXIT THEN LOOP DROP 0 ;

EXIT
: OTHEREXP ( cur - new) #EXP @ 1- FOR DUP I - IF
    DROP R> EXIT THEN NEXT ( Never completes here) ;

( 4826 LIST)
( STEP performs one step/epoch of a "stream of intelligence". This one is not very bright at all.)

( Stream of Intelligence)
: STEP PREVEXP @ MOOD @ BORED = IF OTHEREXP 0 #SATIS !
    THEN DUP CUREXP ! DUP PREDICT EXPECTED !
        ENACT DUP RESULT ! +INT CURINT !
RESULT @ EXPECTED @ - IF FRUST MOOD ! 0 #SATIS !
    ELSE SATIS MOOD ! #SATIS TALLY THEN
#SATIS @ BOREDOMLEVEL @ < NOT IF BORED MOOD ! THEN
CUREXP @ PREVEXP ! ;