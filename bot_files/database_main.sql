CREATE TABLE server_constants 
    (guild_id BIGINT,
    tourney_status SMALLINT,
    tourney_1 VARCHAR(255),
    log_channel_1 BIGINT,
    clan_enable_1 SMALLINT,
    tourney_2 VARCHAR(255),
    log_channel_2 BIGINT,
    clan_enable_2 SMALLINT,
    tourney_3 VARCHAR(255),
    log_channel_3 BIGINT,
    clan_enable_3 SMALLINT,
    ranked_enable INT,
    ranked_channel BIGINT,
    admins VARCHAR(65535),
    member_log_channel BIGINT);

CREATE TABLE rank_system
    (player_id BIGINT,
    player_name VARCHAR(255),
    player_rank VARCHAR(255),
    rank_value SMALLINT,
    points INT,
    wins INT,
    matches_played INT,
    streak INT,
    floor INT);

CREATE TABLE common_system
    (player_id BIGINT,
    player_name VARCHAR(255),
    player_rank VARCHAR(255),
    rank_value SMALLINT,
    points INT,
    wins INT,
    matches_played INT,
    streak INT,
    floor INT);

CREATE TABLE bans
    (rank_bans BIGINT
    );

CREATE TABLE clans
    (clan_name VARCHAR(255),
    points INT,
    played INT,
    leaders VARCHAR(255),
    date_created VARCHAR(255),
    avatar VARCHAR(255));


CREATE TABLE registered
    (player_id BIGINT,
    clan_1 VARCHAR(255),
    badges VARCHAR(65535),
    embed_colour VARCHAR(255),
    date_1 VARCHAR(255),
    scraps INT,
    banner_pieces INT,
    wishes INT,
    banner_count INT,
    current_banner VARCHAR(255),    
    banner_list VARCHAR(65535),
    banner_border VARCHAR(255),
    border_count INT,
    border_list VARCHAR(65535),
    avatar_border VARCHAR(255),
    avaborder_count INT,
    avaborder_list VARCHAR(65535),
    title VARCHAR(255),
    title_count INT,
    title_list VARCHAR(65535)
    );

CREATE TABLE banners
    (banner_name VARCHAR(255),
    banner_place VARCHAR(255),
    price INT,
    rank VARCHAR(255),
    shop VARCHAR(255)
    );

CREATE TABLE borders
    (border_name VARCHAR(255),
    border_place VARCHAR(255),
    price INT,
    rank VARCHAR(255),
    shop VARCHAR(255)
    );

CREATE TABLE avatar_borders
    (banner_name VARCHAR(255),
    avatar_place VARCHAR(255),
    price INT,
    rank VARCHAR(255),
    shop VARCHAR(255)
    );

CREATE TABLE titles
    (banner_name VARCHAR(255),
    title_place VARCHAR(255),
    price INT,
    shop VARCHAR(255));

CREATE TABLE market
    (item_id VARCHAR(255),
    item_name VARCHAR(255),
    item_type VARCHAR(255),
    price INT,
    rank VARCHAR(255),
    added TIMESTAMP DEFAULT NOW(),
    player_id BIGINT
    );



CREATE TABLE market
    (item_id VARCHAR(255),
    item_name VARCHAR(255),
    item_type VARCHAR(255),
    rank VARCHAR(255),
    added TIMESTAMP DEFAULT NOW(),
    player_id BIGINT
    );

CREATE TABLE limited
    (
    item_name VARCHAR(255),
    item_type VARCHAR(255),
    price INT,
    rank VARCHAR(255),
    added TIMESTAMP,
    delete_time BIGINT
    );


CREATE TABLE gamble
    (
    player_name  VARCHAR(255),
    player_id BIGINT,
    played INT,
    won INT,
    rate INT,
    highest INT,
    total INT,
    net INT
    );


CREATE TABLE casual
    (player_id BIGINT,
    player_name VARCHAR(255),
    points INT,
    wins INT,
    matches_played INT,
    streak INT
    );

CREATE TABLE tiles
    (tileid VARCHAR(255),
    player_id BIGINT,
    x INT,
    y INT,
    effect VARCHAR(255),
    item VARCHAR(255)
    );

CREATE TABLE spawn
    (player_id BIGINT,
    tiles VARCHAR(65535),
    items VARCHAR(255),
    effect VARCHAR(255),
    players VARCHAR(65535),
    captured VARCHAR(65535),
    econ INT
    );

CREATE TABLE odditites
    (odditites_name VARCHAR(255),
    odditites_place VARCHAR(255),
    price INT,
    odditites_display VARCHAR(255),
    odditites_desc VARCHAR(255),
    shop VARCHAR(255)
    );