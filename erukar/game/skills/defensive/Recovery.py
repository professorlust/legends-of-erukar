class Recovery:
    '''
    Recovery grants health over time which stacks with HoT spells. The rate is a percentage of max
    health (1.875% per level up to a max of 10% of health). If the amount of health per turn is
    less than 1, the player instead gains one health every X turns, where 
        
        X = floor(1 / (max_health * percentage))

    '''
    pass
