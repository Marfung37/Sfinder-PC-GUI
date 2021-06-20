# Sfinder-PC-GUI
A gui for pc-based research based on the sfinder program made by knewjade
Some libraries to download if you want full functionality
* For finding true minimal [sfinder-strict-minimal](https://github.com/eight04/sfinder-strict-minimal)
* For handling fumen scripts [fumen api](https://github.com/knewjade/tetris-fumen)

## Saves Tab
### Pieces
The same as [sfinder's pattern syntax](https://knewjade.github.io/sfinder-docs/contents/patterns.html)
* Connect elements with comma
    * ``I, T, S, Z`` → ITSZ 1 way
    * ``[SZ], O, [JL]`` → SOJ, SOL, ZOJ, ZOL 4 ways
    * ``L, *`` → LT, LI, LJ, LL, LS, LZ, LO 7 ways
    * You can omit the comma that connects the pieces.
        * ``T, I, O`` →　TIO
        * ``S, Z, *p3`` →　SZ, *p3
* Element Rule
    * ``I`` : I only: 1 way
    * ``[SZLJ]`` : Select one from SZJL: 4 ways
    * ``[^TI]`` : Select one from other than TI: 5 ways
    * ``[SZLJ]p2`` : Select 2 from SZLJ Permutation: 12 ways
    * ``*`` (Asterisk): Equivalent to [TIJLSZO]: 7 ways
    * ``*p3`` : [TIJLSZO] Equivalent to p3: 7P3 = 210 ways
    * ``[SZLJ]!`` : [SZLJ] Equivalent to p4: 4P4 = 4! = 24 ways
    * ``*!`` : [TIJLSZO] Equivalent to p7: 7P7 = 7! = 5040 ways
* You may concatate multiple patterns with ``;``
    * ``T,*; I,*`` : TT,TI,TL,TJ,TS,TZ,TO; IT,II,IL,IJ,IS,IZ,IO: 14 ways
* For saves, you must end with a bag (doesn't need to be a 7bag)
    * ``[TJO],*p4`` - the ``*p4`` is the ending bag

### Wanted Saves
* ``I, LS, LSZ`` - does each wanted saves separately
* ``^S`` - avoider, possible to avoid S
    * matches ``[LS, LZ]``
    * fails ``[LS, SZ]``
* ``!T`` - NOT, gives inverse result: always unable to save T
    * matches ``[L, S] [LSZO]``
    * fails ``[T, I] [TLSZ]``
* ``T&&S`` - AND, both T&&S are saveable
    * matches ``[T, S, Z] [TSZ]``
    * fails ``[S, Z] [SZO] [TZ]``
* ``T||S`` - OR, at least one of T or S are saveable
    * matches ``[T, Z] [TSO] [LSO]``
    * fails ``[I, L, O] [LZO]``
* ``!(T&&S)||L`` - does T&&S first before rest of expression
   * With ^(T&&S) it distributes the avoider to T and S and does || instead (De Morgan's Law)
* ``LSZ`` - queue, all of L,S,Z are in at least one of the saves
    * matches ``[LSZO, TSZO] [TLSZ, LLSZ]``
    * fails ``[L, S, Z] [TSZ, JSZ]``
* ``/^[^T]\*L[^J]\*$/`` - regex queue, a regex expression in ``//``: at least one save has L but not T nor J
    * matches ``[ILSZ, IJSZ] [LL]``
    * fails ``[TLSZ] [LJSZ]``
    * the order of saves always follow TILJSZO
    * Note: this is necessary for the full potential of this syntax
* ``all`` - all saves, it provides all the saves and percentages for them
