\ eliza-gforth.fs
\ Initial gforth-compatible ELIZA port (separate from polyForth aeon.f)

: upc ( c -- c' ) dup [char] a [char] z 1+ within IF 32 - THEN ;

: strip-punct ( c -- c' )
  dup [char] . = over [char] , = or over [char] ! = or over [char] ? = or
  IF drop bl THEN ;

: normalize ( c-addr u -- c-addr u )
  2dup over + swap ?DO
    I c@ strip-punct upc I c!
  LOOP ;

: contains? ( hay-addr hay-u needle-addr needle-u -- f )
  search nip nip ;

create input-buf 256 allot
create work-buf 256 allot

: read-line-into ( -- u )
  input-buf 255 accept input-buf swap ;

: copy-to-work ( c-addr u -- c-addr u )
  2dup work-buf swap move work-buf swap ;

: .resp ( c-addr u -- ) type cr ;

: reply-for ( c-addr u -- )
  2dup s" OFF" contains? IF 2drop s" OK THEN, GOODBYE!" .resp bye THEN
  2dup s" MOTHER" contains? IF 2drop s" TELL ME MORE ABOUT YOUR FAMILY." .resp EXIT THEN
  2dup s" FATHER" contains? IF 2drop s" HOW IS YOUR RELATIONSHIP WITH YOUR FATHER?" .resp EXIT THEN
  2dup s" DREAM" contains? IF 2drop s" WHAT DOES THAT DREAM SUGGEST TO YOU?" .resp EXIT THEN
  2dup s" SAD" contains? IF 2drop s" DID YOU THINK THEY MIGHT NOT BE SAD?" .resp EXIT THEN
  2dup s" HAPPY" contains? IF 2drop s" I AM GLAD THAT YOU FEEL HAPPY." .resp EXIT THEN
  2dup s" I FEEL" contains? IF 2drop s" TELL ME MORE ABOUT THOSE FEELINGS." .resp EXIT THEN
  2dup s" I THINK" contains? IF 2drop s" DO YOU REALLY THINK SO?" .resp EXIT THEN
  2dup s" YOU ARE" contains? IF 2drop s" WHAT MAKES YOU THINK I AM THAT?" .resp EXIT THEN
  2dup s" WHY" contains? IF 2drop s" WHY DO YOU ASK?" .resp EXIT THEN
  2dup s" NO" contains? IF 2drop s" ARE YOU SAYING 'NO' JUST TO BE CONTRARY?" .resp EXIT THEN
  2dup s" YES" contains? IF 2drop s" YOU SEEM SURE." .resp EXIT THEN
  2dup s" COMPUTER" contains? IF 2drop s" DO COMPUTERS WORRY YOU?" .resp EXIT THEN
  2dup s" INTERNET" contains? IF 2drop s" DOES THE INTERNET WORRY YOU?" .resp EXIT THEN
  2drop s" PLEASE ELABORATE ON THAT POINT." .resp ;

: eliza-gforth ( -- )
  cr s" TELL ME ABOUT IT." .resp
  BEGIN
    read-line-into copy-to-work normalize
    2dup nip 0= IF
      2drop s" DON'T BE SHY, I WON'T BITE!" .resp
    ELSE
      reply-for
    THEN
  AGAIN ;

: ELIZA eliza-gforth ;

cr .( gforth ELIZA ready. Type ELIZA and enter OFF to quit. ) cr
