person(greg).
person(susan).

son(greg,david).
son(david,jack).

daughter(kim,david).
daughter(steph,david).

child(X,Y) :- son(X,Y).
child(X,Y) :- daughter(X,Y).

lower(List, V, Lower) :- 
    findall(Elem, (member(Elem, List), Elem < V), Lower).

upper(List, V, Upper) :- 
    findall(Elem, (member(Elem, List), Elem > V), Upper).

equal(List, V, Equal) :- 
    findall(Elem, (member(Elem, List), Elem = V), Equal).

quick_sort([],[]).
quick_sort([V|Rest], Sorted) :-
    lower(Rest, V, Lower),
    equal([V|Rest], V, Equal),
    upper(Rest, V, Upper),
    quick_sort(Lower, SortedLower),
    quick_sort(Upper, SortedUpper),
    append(SortedLower, Equal, SortedLowerEqual),
    append(SortedLowerEqual, SortedUpper, Sorted).
