from adjudicator.orders import *

global cycle, recursion_hits, uncertain
cycle: list[Order] = []
recursion_hits: int
uncertain: bool

def adjudicate(order: Order, optimistic: bool) -> bool:
    adjudicate_strengths(order, optimistic)

    if isinstance(order, Move):
        return adjudicate_move(order, optimistic)
    elif isinstance(order, Support):
        return adjudicate_support(order, optimistic)
    elif isinstance(order, Convoy):
        return adjudicate_convoy(order, optimistic)
    else:
        return False

def adjudicate_move(order: Move, optimistic: bool) -> bool:
    # Check if head-to-head
    if order.unit is not None:
        if order.destination.unit is not None and hasattr(order.destination.unit, "order") and isinstance(order.destination.unit.order, Move):
            if order.destination == order.destination.unit.order.destination:
                order.head_to_head = True

    # return order.unit.attack_strength > order.destination.hold_strength and order.unit.attack_strength > prevent_strength
    return False

def adjudicate_support(order: Support, optimistic: bool) -> bool:
    # TODO: Implement support adjudication logic
    return False

def adjudicate_convoy(order: Convoy, optimistic: bool) -> bool:
    # TODO: Implement convoy adjudication logic
    return False

def adjudicate_path(order, optimistic: bool) -> bool:
    # TODO: Implement path adjudication logic
    return False

def adjudicate_strengths(order: Order, optimistic: bool) -> None:
    order.unit.attack_strength = adjudicate_attack_strength(order, optimistic)
    order.unit.location.hold_strength = adjudicate_hold_strength(order, optimistic)
    order.unit.defend_strength = adjudicate_defend_strength(order, optimistic)
    order.unit.prevent_strength = adjudicate_prevent_strength(order, optimistic)

def adjudicate_attack_strength(order: Order, optimistic: bool) -> int:
    if isinstance(order, Move):
        adjudicate_path(order, optimistic)
        if not order.path:
            return 0
        elif not order.destination.unit is None or (order.head_to_head and order.destination.unit.order)
    return 0

def adjudicate_hold_strength(order: Order, optimistic: bool) -> int:
    return False

def adjudicate_defend_strength(order: Order, optimistic: bool) -> int:
    return False

def adjudicate_prevent_strength(order: Order, optimistic: bool) -> int:
    return False


def resolve(order, optimistic):
    global cycle, recursion_hits, uncertain
    if order.resolved:
        return order.resolution

    if order in cycle:
        # We already concluded that this order is in a cycle
        # which we cannot yet resolve.
        # Result is based on uncertain information.
        uncertain = True
        return optimistic # Success when optimistic,
                          # fail when pessimistic.

    if order.visited:
        # We hit cyclic dependency.
        cycle.append(order)
        recursion_hits += 1
        uncertain = True
        return optimistic

    order.visited = True # Prevent endless recursion.
    old_cycle_len = len(cycle)
    old_recursion_hits = recursion_hits
    old_uncertain = uncertain
    uncertain = False
    optimistic_result = adjudicate(order, True)
    # Try to avoid a second adjudication for performance.
    pessimistic_result = adjudicate(order, False) if uncertain and optimistic_result else optimistic_result
    order.visited = False
    
    if optimistic_result == pessimistic_result:
        # We have a single resolution. Wipe out any
        # cycle information that was found in recursion.
        del cycle[old_cycle_len:]
        recursion_hits = old_recursion_hits
        # The uncertain variable must be unaltered, because
        # order is resolved now.
        uncertain = old_uncertain
        # Store the result and return it.
        order.resolution = optimistic_result
        order.resolved = True
        return optimistic_result

    if order in cycle:
        # We returned from recursion, where this order hit the
        # cycle and we didn't get a single resolution.
        recursion_hits -= 1

    if recursion_hits == old_recursion_hits:
        # We have sufficiently retreated from recursion such
        # that this order was the ancestor of the whole cycle.
        # Apply backup rule on all orders in cycle.
        backup_rule(cycle[old_cycle_len:])
        del cycle[old_cycle_len:]
        uncertain = old_uncertain
        # The backup rule might not have resolved this order.
        return resolve(order, optimistic)

    # We are returning from a situation where a cycle was
    # detected. However, this order is not the ancestor of the
    # whole cycle. We further retreat from recursion.
    if not order in cycle:
        cycle.append(order)
    return optimistic

def backup_rule(orders: list[Order]) -> None:
    for order in orders:
        pass











def resolve_orders(orders: list[Order]) -> None:
    """Resolves all orders"""

    for order in orders:
        resolve(order, True)


def calculate_attack_strength(move_order: Move, orders: list[Order]) -> int:
    strength: int = 1

    # Check how many are supporting
    for order in orders:
        if isinstance(order, Support) and order.supported_order == move_order:
            strength += 1
    
    return strength
