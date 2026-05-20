\ ideal-gforth.fs
\ gforth port of the simplified IDEAL model

10 constant MEXP
10 constant MRES
6  constant MMOOD
100 constant MINT

\ mood ids
0 constant MNOTH
1 constant SATIS
2 constant FRUST
3 constant BORED
4 constant PAIN
5 constant PLEAS

\ experiment/result ids
0 constant E0
1 constant E1
2 constant E2
0 constant R0
1 constant R1
2 constant R2

variable #EXP
variable #RES
variable #MOOD
variable #INT

variable PREVEXP
variable CUREXP
variable MOOD
variable #SATIS
variable BOREDOMLEVEL
variable EXPECTED
variable RESULT
variable CURINT

create int-exp MINT cells allot
create int-res MINT cells allot

: init-ideal ( -- )
  2 #EXP !
  2 #RES !
  5 #MOOD !
  2 BOREDOMLEVEL !
  0 #SATIS !
  E1 PREVEXP !
  MNOTH MOOD !
  1 #INT ! ;

: .EXP ( e -- )
  dup E1 = IF drop s" E1" type EXIT THEN
  dup E2 = IF drop s" E2" type EXIT THEN
  drop s" E0" type ;

: .RES ( r -- )
  dup R1 = IF drop s" R1" type EXIT THEN
  dup R2 = IF drop s" R2" type EXIT THEN
  drop s" R0" type ;

: .MOOD ( m -- )
  dup SATIS = IF drop s" SelfSatisfied" type EXIT THEN
  dup FRUST = IF drop s" Frustrated" type EXIT THEN
  dup BORED = IF drop s" Bored" type EXIT THEN
  dup PAIN  = IF drop s" Pained" type EXIT THEN
  dup PLEAS = IF drop s" Pleased" type EXIT THEN
  drop s" Nothing" type ;

: .INT ( i -- )
  dup 0= IF drop s" [null]" type exit THEN
  dup cells int-exp + @ .EXP
  s" ->" type
  cells int-res + @ .RES ;

: ?INT ( iE iR -- iI|0 )
  #INT @ 1 ?DO
    2dup
    I cells int-exp + @ =
    swap I cells int-res + @ = and
    IF 2drop I unloop exit THEN
  LOOP
  2drop 0 ;

: +INT ( iE iR -- iI )
  2dup ?INT dup 0<> IF nip nip exit THEN drop
  #INT @ dup MINT = abort" Too many prim interactions!"
  dup >r
  over r@ cells int-exp + !
  swap r@ cells int-res + !
  #INT @ 1+ #INT !
  2drop
  r> ;

: PREDICT ( exp -- res )
  #INT @ 1 ?DO
    dup I cells int-exp + @ = IF
      drop I cells int-res + @ unloop exit
    THEN
  LOOP
  drop R0 ;

: ENACT ( -- res )
  CUREXP @ E1 = IF R1 ELSE R2 THEN ;

: OTHEREXP ( cur -- new )
  dup E1 = IF drop E2 ELSE drop E1 THEN ;

: STEP ( -- )
  PREVEXP @
  MOOD @ BORED = IF OTHEREXP 0 #SATIS ! THEN
  dup CUREXP !
  dup PREDICT EXPECTED !
  ENACT dup RESULT !
  +INT CURINT !

  RESULT @ EXPECTED @ <> IF
    FRUST MOOD !
    0 #SATIS !
  ELSE
    SATIS MOOD !
    #SATIS @ 1+ #SATIS !
  THEN

  #SATIS @ BOREDOMLEVEL @ >= IF BORED MOOD ! THEN
  CUREXP @ PREVEXP ! ;

: RUN ( -- )
  init-ideal
  20 0 DO
    STEP cr
    I . s" : " type
    CURINT @ dup . space .INT space
    EXPECTED @ .RES space
    MOOD @ .MOOD
  LOOP cr ;

init-ideal
cr .( ideal-gforth ready. Run RUN ) cr
