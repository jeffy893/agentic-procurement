def evaluate_purchase(proposed_item, current_inventory_item):
    if proposed_item['TechnicalSpecs'] != current_inventory_item['TechnicalSpecs']:
        return 'REJECTED: Specs Mismatch'
    
    if proposed_item['Price'] < 1000:
        return 'APPROVED'
    else:
        return 'PENDING MANAGER'