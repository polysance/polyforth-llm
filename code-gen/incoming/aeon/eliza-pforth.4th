: within over - >r - r> u< ;

: upc dup 97 123 within IF 32 - THEN ;

: strip-punct
  dup 46 = over 44 = or over 33 = or over 63 = or
  IF drop 32 THEN ;

: normalize
  over + swap ?DO
    I c@ strip-punct upc I c!
  LOOP ;

: contains?
  search nip nip ;

create input-buf 256 allot
create work-buf 256 allot

: read-line-into
  input-buf 255 accept input-buf swap ;

: copy-to-work
  2dup work-buf swap move work-buf swap ;

: .resp type cr ;

: reply-for
  2dup s" OFF" contains? IF 2drop s" OK THEN, GOODBYE!" .resp FALSE EXIT THEN
  2dup s" MOTHER" contains? IF 2drop s" TELL ME MORE ABOUT YOUR FAMILY." .resp TRUE EXIT THEN
  2dup s" FATHER" contains? IF 2drop s" HOW IS YOUR RELATIONSHIP WITH YOUR FATHER?" .resp TRUE EXIT THEN
  2dup s" DREAM" contains? IF 2drop s" WHAT DOES THAT DREAM SUGGEST TO YOU?" .resp TRUE EXIT THEN
  2dup s" SAD" contains? IF 2drop s" DID YOU THINK THEY MIGHT NOT BE SAD?" .resp TRUE EXIT THEN
  2dup s" HAPPY" contains? IF 2drop s" I AM GLAD THAT YOU FEEL HAPPY." .resp TRUE EXIT THEN
  2dup s" I FEEL" contains? IF 2drop s" TELL ME MORE ABOUT THOSE FEELINGS." .resp TRUE EXIT THEN
  2dup s" I THINK" contains? IF 2drop s" DO YOU REALLY THINK SO?" .resp TRUE EXIT THEN
  2dup s" YOU ARE" contains? IF 2drop s" WHAT MAKES YOU THINK I AM THAT?" .resp TRUE EXIT THEN
  2dup s" WHY" contains? IF 2drop s" WHY DO YOU ASK?" .resp TRUE EXIT THEN
  2dup s" NO" contains? IF 2drop s" ARE YOU SAYING NO JUST TO BE CONTRARY?" .resp TRUE EXIT THEN
  2dup s" YES" contains? IF 2drop s" YOU SEEM SURE." .resp TRUE EXIT THEN
  2dup s" COMPUTER" contains? IF 2drop s" DO COMPUTERS WORRY YOU?" .resp TRUE EXIT THEN
  2dup s" INTERNET" contains? IF 2drop s" DOES THE INTERNET WORRY YOU?" .resp TRUE EXIT THEN
  2drop s" PLEASE ELABORATE ON THAT POINT." .resp TRUE ;

: ELIZA
  cr s" TELL ME ABOUT IT." .resp
  BEGIN
    read-line-into copy-to-work normalize
    2dup nip 0= IF 2drop s" DONT BE SHY, I WONT BITE!" .resp TRUE
    ELSE
      reply-for
    THEN
  WHILE
  REPEAT ;
