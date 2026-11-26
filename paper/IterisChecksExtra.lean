import Lean

/-!
Additional finite checks for "Rational Numerals and Carry Geometry in Iteris".

This file is self-contained and shares the base definitions from
`IterisChecksV02.lean`. It uses a separate namespace so both files can coexist.
-/

namespace IterisExtra

/-! ## Base definitions (as in IterisChecksV02.lean) -/

/-- Bits encode the strokes p1, p2, p3, p4, and p6, in that order. -/
def digitMask : Nat -> Nat
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 4
  | 4 => 8
  | 5 => 9
  | 6 => 16
  | 7 => 17
  | 8 => 18
  | 9 => 19
  | _ => 0

def strokeDistance (a b : Nat) : Nat :=
  ((List.range 5).filter fun bit =>
    digitMask a / 2 ^ bit % 2 != digitMask b / 2 ^ bit % 2).length

def digitAt (n position : Nat) : Nat :=
  n / 10 ^ position % 10

def blockDistance (n m : Nat) : Nat :=
  ((List.range 4).map fun position =>
    strokeDistance (digitAt n position) (digitAt m position)).sum

/-! ## Theorem 2: counts that the text states but the first file does not check -/

/-- The digit graph has thirteen edges. -/
theorem digitEdgeCount :
    ((List.range 10).map fun a =>
      ((List.range 10).filter fun b =>
        decide (a < b) && strokeDistance a b == 1).length).sum = 13 := by
  native_decide

/-- Diameter 4, attained exactly by the pairs {3,9}, {4,9}, {5,8}. -/
theorem digitDiameter :
    (List.range 10).all (fun a =>
      (List.range 10).all (fun b =>
        decide (strokeDistance a b <= 4) &&
        ((strokeDistance a b == 4) ==
          ((a == 3 && b == 9) || (a == 9 && b == 3) ||
           (a == 4 && b == 9) || (a == 9 && b == 4) ||
           (a == 5 && b == 8) || (a == 8 && b == 5))))) = true := by
  native_decide

/-! ## Total and mean carry cost -/

/-- The closed decade tour 0 -> 1 -> ... -> 9 -> 0 costs 18 strokes. -/
theorem decadeTour :
    ((List.range 10).map fun d => strokeDistance d ((d + 1) % 10)).sum = 18 := by
  native_decide

/-- Counting 0000 -> 9999 costs 2 * (10^4 - 1) - 3 * 4 = 19986 strokes. -/
theorem totalCountingCost :
    ((List.range 9999).map fun n => blockDistance n (n + 1)).sum = 19986 := by
  native_decide

/-! ## Parity obstruction to a one-stroke ordering -/

/-- Number of strokes in a node (distance to the bare stem). -/
def strokeCount (n : Nat) : Nat :=
  blockDistance n 0

/-- 5008 nodes have an even stroke count and 4992 an odd one. -/
theorem parityClasses :
    ((List.range 10000).filter fun n => strokeCount n % 2 == 0).length = 5008 := by
  native_decide

/-! ## An explicit minimum-cost ordering of all 10000 nodes -/

/-- The path 1,5,4,0,2,8,9,7,6 through every digit except 3. -/
def pathDigit : Nat -> Nat
  | 0 => 1
  | 1 => 5
  | 2 => 4
  | 3 => 0
  | 4 => 2
  | 5 => 8
  | 6 => 9
  | 7 => 7
  | _ => 6

theorem pathDigitIsPath :
    (List.range 8).all (fun i =>
      strokeDistance (pathDigit i) (pathDigit (i + 1)) == 1) = true := by
  native_decide

def concatMap {α : Type} (f : Nat -> List α) : List Nat -> List α
  | [] => []
  | x :: xs => f x ++ concatMap f xs

/-- Boustrophedon order on k free positions, from all 1s to all 6s. -/
def snake : Nat -> List (List Nat)
  | 0 => [[]]
  | k + 1 =>
      concatMap (fun i =>
        (if i % 2 == 0 then snake k else (snake k).reverse).map
          fun rest => pathDigit i :: rest) (List.range 9)

/-- Put digit 3 at the positions in `mask` and the free digits elsewhere. -/
def assemble (mask : Nat) : Nat -> Nat -> List Nat -> Nat
  | 0, _, _ => 0
  | fuel + 1, pos, free =>
      if mask / 2 ^ pos % 2 == 1 then
        3 * 10 ^ pos + assemble mask fuel (pos + 1) free
      else
        match free with
        | [] => assemble mask fuel (pos + 1) []
        | d :: rest => d * 10 ^ pos + assemble mask fuel (pos + 1) rest

def freeCount (mask : Nat) : Nat :=
  ((List.range 4).filter fun pos => mask / 2 ^ pos % 2 == 0).length

def piece (mask : Nat) : List Nat :=
  (snake (freeCount mask)).map fun free => assemble mask 4 0 free

/-- Reflected binary Gray code on the sixteen sets of positions holding a 3. -/
def grayMasks : List Nat :=
  [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]

def strokeOrderAux : Nat -> List Nat -> List Nat
  | _, [] => []
  | j, mask :: rest =>
      (if j % 2 == 0 then piece mask else (piece mask).reverse) ++
        strokeOrderAux (j + 1) rest

def strokeOrder : List Nat :=
  strokeOrderAux 0 grayMasks

theorem strokeOrderLength : strokeOrder.length = 10000 := by
  native_decide

/-- With the length, this makes `strokeOrder` a permutation of 0000..9999. -/
theorem strokeOrderCovers :
    (List.range 10000).all (fun n => strokeOrder.contains n) = true := by
  native_decide

/-- Total cost 10^4 + 2^4 - 2, meeting the parity lower bound. -/
theorem strokeOrderCost :
    ((strokeOrder.zip (strokeOrder.drop 1)).map fun p =>
      blockDistance p.1 p.2).sum = 10014 := by
  native_decide

theorem strokeOrderEnds :
    (strokeOrder.head?, strokeOrder.reverse.head?) = (some 1111, some 3111) := by
  native_decide

/-- Closing the ordering into a cycle costs two more strokes: 10016 in all. -/
theorem strokeOrderClosingStep : blockDistance 3111 1111 = 2 := by
  native_decide

/-! ## Theorem 1 on a finite range -/

def blockBase : Nat := 10000

def valuation (p : Nat) : Nat -> Nat -> Nat
  | 0, _ => 0
  | fuel + 1, n =>
      if n != 0 && n % p == 0 then 1 + valuation p fuel (n / p) else 0

def coprimePart (q : Nat) : Nat :=
  q / (2 ^ valuation 2 q q * 5 ^ valuation 5 q q)

def prefixLength (q : Nat) : Nat :=
  (max (valuation 2 q q) (valuation 5 q q) + 3) / 4

/-- Multiplicative order of g modulo M, for gcd(g, M) = 1. -/
def mulOrder (g M : Nat) : Nat :=
  (((List.range M).map fun h => h + 1).find? fun h =>
    g ^ h % M == 1 % M).getD 0

def periodLength (q : Nat) : Nat :=
  let L := mulOrder 10 (coprimePart q)
  L / Nat.gcd L 4

/-- The remainder r_j of the block division rule. -/
def blockRemainder (p q : Nat) : Nat -> Nat
  | 0 => p % q
  | j + 1 => blockBase * blockRemainder p q j % q

/-- The predicted prefix and period are exactly the first repeat. -/
def expansionCheck (p q : Nat) : Bool :=
  let t := prefixLength q
  let l := periodLength q
  if coprimePart q == 1 then
    blockRemainder p q t == 0 &&
      (t == 0 || blockRemainder p q (t - 1) != 0)
  else
    l == mulOrder blockBase (coprimePart q) &&
    blockRemainder p q t != 0 &&
    blockRemainder p q t == blockRemainder p q (t + l) &&
    (t == 0 || blockRemainder p q (t - 1) != blockRemainder p q (t - 1 + l)) &&
    (List.range l).all (fun h =>
      h == 0 || blockRemainder p q t != blockRemainder p q (t + h))

/-- Theorem 1 for every reduced p/q in [0, 1) with q < 150. -/
theorem rationalLengths :
    (List.range 150).all (fun q =>
      q == 0 || (List.range q).all (fun p =>
        Nat.gcd p q != 1 || expansionCheck p q)) = true := by
  native_decide

/-- One-node cycles occur exactly when the coprime part divides 9999. -/
theorem oneNodeCycles :
    (List.range 2000).all (fun M =>
      M == 0 || Nat.gcd M 10 != 1 ||
        ((mulOrder blockBase M == 1) == (9999 % M == 0))) = true := by
  native_decide

end IterisExtra
