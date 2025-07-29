from adjudicator.orders import *

global cycle, recursion_hits, uncertain
cycle: list[Order] = []

def adjudicate(order) -> bool:
    return False

def resolve(order: Order) -> bool:
    """Generic order resolution not dependent on exterior context"""
    

    return False

# def resolve(order, optimistic):
#     global cycle, recursion_hits, uncertain
#     if order.resolved:
#         return order.resolution

#     if order in cycle:
#         # We already concluded that this order is in a cycle
#         # which we cannot yet resolve.
#         # Result is based on uncertain information.
#         uncertain = True
#         return optimistic # Success when optimistic,
#                           # fail when pessimistic.

#     if order.visited:
#         # We hit cyclic dependency.
#         cycle.append(order)
#         recursion_hits += 1
#         uncertain = True
#         return optimistic

#     order.visited = True # Prevent endless recursion.
#     old_cycle_len = len(cycle)
#     old_recursion_hits = recursion_hits
#     old_uncertain = uncertain
#     uncertain = False
#     opt_result = adjudicate(order, True)
#     # Try to avoid a second adjudication for performance.
#     pes_result = adjudicate(order, False) if uncertain and opt_result else opt_result
#     order.visited = False
    
#     if opt_result == pes_result:
#         # We have a single resolution. Wipe out any
#         # cycle information that was found in recursion.
#         del cycle[old_cycle_len:]
#         recursion_hits = old_recursion_hits
#         # The uncertain variable must be unaltered, because
#         # order is resolved now.
#         uncertain = old_uncertain
#         # Store the result and return it.
#         order.resolution = opt_result
#         order.resolved = True
#         return opt_result

#     if order in cycle:
#         # We returned from recursion, where this order hit the
#         # cycle and we didn't get a single resolution.
#         recursion_hits -= 1

#     if recursion_hits == old_recursion_hits:
#         # We have sufficiently retreated from recursion such
#         # that this order was the ancestor of the whole cycle.
#         # Apply backup rule on all orders in cycle.
#         backup_rule(cycle[old_cycle_len:])
#         del cycle[old_cycle_len:]
#         uncertain = old_uncertain
#         # The backup rule might not have resolved this order.
#         return resolve(order, optimistic)

#     # We are returning from a situation where a cycle was
#     # detected. However, this order is not the ancestor of the
#     # whole cycle. We further retreat from recursion.
#     if not order in cycle:
#         cycle.add(order)
#     return optimistic