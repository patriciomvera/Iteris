import Lean

/-!
Finite checks for Rational Numerals and Carry Geometry in Iteris.
Run with Lean 4 using "lean IterisChecksV02.lean". No Mathlib is required.

The graph and carry checks concern one digit or one four-digit node.
The expansion checks are concrete examples. The manuscript gives the
general proofs, including the optimality bound for every width.
-/

namespace Iteris

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

def digitPairs : List (Nat × Nat) :=
  (List.range 10).flatMap fun a =>
    ((List.range 10).filter fun b => decide (a < b)).map fun b => (a, b)

theorem digitEdgeCount :
    (digitPairs.filter fun pair => strokeDistance pair.1 pair.2 == 1).length = 13 := by
  native_decide

theorem digitDiameter :
    digitPairs.all (fun pair => decide (strokeDistance pair.1 pair.2 <= 4)) = true := by
  native_decide

theorem diametralDigitPairs :
    (digitPairs.filter fun pair => strokeDistance pair.1 pair.2 == 4) =
      [(3, 9), (4, 9), (5, 8)] := by
  native_decide

/-- A Hamming geodesic can be built by repeatedly taking a closer valid digit. -/
theorem digitGeodesicSteps :
    (List.range 10).all (fun a =>
      (List.range 10).all (fun b =>
        (a == b) || (List.range 10).any (fun c =>
          (strokeDistance a c == 1) &&
          (strokeDistance c b + 1 == strokeDistance a b)))) = true := by
  native_decide

/-- Positions in a node are numbered from the units digit. -/
def digitAt (n position : Nat) : Nat :=
  n / 10 ^ position % 10

def blockDistance (n m : Nat) : Nat :=
  ((List.range 4).map fun position =>
    strokeDistance (digitAt n position) (digitAt m position)).sum

def successorDigitCost : Nat -> Nat
  | 0 => 1
  | 1 => 2
  | 2 => 2
  | 3 => 2
  | 4 => 1
  | 5 => 3
  | 6 => 1
  | 7 => 2
  | 8 => 1
  | _ => 0

/-- The predicted cost of a successor within the given decimal width. -/
def carryCost : Nat -> Nat -> Nat
  | 0, _ => 0
  | width + 1, n =>
      if n % 10 == 9 then 3 + carryCost width (n / 10)
      else successorDigitCost (n % 10)

theorem successorDigitCosts :
    (List.range 9).all (fun d =>
      strokeDistance d (d + 1) == successorDigitCost d) = true := by
  native_decide

theorem resetNineCost : strokeDistance 9 0 = 3 := by
  decide

/-- The carry formula agrees with direct stroke counts for 0000 through 9998. -/
theorem fourDigitCarryCosts :
    (List.range 9999).all (fun n =>
      blockDistance n (n + 1) == carryCost 4 n) = true := by
  native_decide

theorem fourDigitMaximum :
    (List.range 9999).all (fun n =>
      decide (blockDistance n (n + 1) <= 12) &&
      ((blockDistance n (n + 1) == 12) == (n == 5999))) = true := by
  native_decide

def fourDigitCarryHistogram : List Nat :=
  let counts := (List.range 9999).foldl (fun (counts : Array Nat) n =>
    let cost := blockDistance n (n + 1)
    counts.set! cost (counts[cost]! + 1)) (Array.replicate 13 0)
  counts.toList

theorem fourDigitCarryDistribution :
    fourDigitCarryHistogram = [0, 4000, 4000, 1000, 400, 400, 100, 40, 40, 10, 4, 4, 1] := by
  native_decide

/-- Block division records each output digit together with the new remainder. -/
def divisionSteps (base denominator : Nat) : Nat -> Nat -> List (Nat × Nat)
  | 0, _ => []
  | steps + 1, remainder =>
      let scaled := base * remainder
      let next := scaled % denominator
      (scaled / denominator, next) :: divisionSteps base denominator steps next

theorem recurringDivisionExamples :
    divisionSteps 10000 6 2 1 = [(1666, 4), (6666, 4)] ∧
    divisionSteps 10000 7 3 1 = [(1428, 4), (5714, 2), (2857, 1)] ∧
    divisionSteps 10000 17 4 1 = [(588, 4), (2352, 16), (9411, 13), (7647, 1)] ∧
    divisionSteps 10000 101 1 1 = [(99, 1)] ∧
    divisionSteps 10000 30000 2 1 = [(0, 10000), (3333, 10000)] := by
  native_decide

/-- Iterate modular multiplication, using fuel to bound the search. -/
def orderSearch (base modulus : Nat) : Nat -> Nat -> Nat -> Option Nat
  | 0, _, _ => none
  | fuel + 1, exponent, residue =>
      let next := residue * base % modulus
      if next == 1 then some exponent
      else orderSearch base modulus fuel (exponent + 1) next

def multiplicativeOrder (base modulus : Nat) : Option Nat :=
  orderSearch base modulus modulus 1 1

theorem representativePeriodLengths :
    multiplicativeOrder 10 7 = some 6 ∧
    multiplicativeOrder 10000 7 = some 3 ∧
    multiplicativeOrder 10 17 = some 16 ∧
    multiplicativeOrder 10000 17 = some 4 ∧
    multiplicativeOrder 10000 101 = some 1 := by
  native_decide

/-- Every digit except 3 appears on this single-stroke path. -/
def digitLine : List Nat := [1, 5, 4, 0, 2, 8, 9, 7, 6]

theorem digitLineCertificate :
    (List.range 10).all (fun d => digitLine.contains d == (d != 3)) = true ∧
    digitLine.length = 9 ∧
    (digitLine.zip (digitLine.drop 1)).all (fun pair =>
      strokeDistance pair.1 pair.2 == 1) = true ∧
    strokeDistance 3 1 = 2 ∧ strokeDistance 3 6 = 2 := by
  native_decide

/-- Reflected binary Gray order for the sets of coordinates fixed to digit 3. -/
def grayFlags : Nat -> List (List Bool)
  | 0 => [[]]
  | width + 1 =>
      let flags := grayFlags width
      (flags.map fun suffix => false :: suffix) ++
        (flags.reverse.map fun suffix => true :: suffix)

/-- Serpentine order on the product of the digit lines, with units read first. -/
def boxOrder : List (List Nat) -> List Nat
  | [] => [0]
  | line :: rest =>
      let suffixOrder := boxOrder rest
      let reversedSuffix := suffixOrder.reverse
      (line.zip (List.range line.length)).flatMap fun (digit, index) =>
        let suffix := if index % 2 == 0 then suffixOrder else reversedSuffix
        suffix.map fun higherDigits => digit + 10 * higherDigits

/-- Even-indexed boxes run forward and odd-indexed boxes run backward. -/
def fourDigitStrokeOrder : List Nat :=
  ((grayFlags 4).zip (List.range 16)).flatMap fun (fixed, index) =>
    let lines := fixed.reverse.map fun value => if value then [3] else digitLine
    let order := boxOrder lines
    if index % 2 == 0 then order else order.reverse

/-- Linear coverage check via a dense visited table. -/
def coversFourDigitNodes (order : List Nat) : Bool :=
  let visited := order.foldl (fun (visited : Array Bool) n =>
    if n < visited.size then visited.set! n true else visited) (Array.replicate 10000 false)
  (order.length == 10000) && visited.toList.all id

theorem strokeOrderCovers : coversFourDigitNodes fourDigitStrokeOrder = true := by
  native_decide

def strokeOrderCosts (order : List Nat) : List Nat :=
  (order.zip (order.drop 1)).map fun pair => blockDistance pair.1 pair.2

def fourDigitStrokeOrderCosts : List Nat := strokeOrderCosts fourDigitStrokeOrder

theorem strokeOrderTotal :
    fourDigitStrokeOrderCosts.sum = 10014 := by
  native_decide

theorem strokeOrderStepCounts :
    (fourDigitStrokeOrderCosts.filter fun c => c == 1).length = 9984 ∧
    (fourDigitStrokeOrderCosts.filter fun c => c == 2).length = 15 := by
  native_decide

theorem strokeOrderEndpoints :
    fourDigitStrokeOrder.head? = some 1111 ∧
    fourDigitStrokeOrder.reverse.head? = some 3111 := by
  native_decide

theorem closedStrokeOrderTotal :
    (strokeOrderCosts (fourDigitStrokeOrder ++ [1111])).sum = 10016 := by
  native_decide

end Iteris
