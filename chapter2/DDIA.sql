-- SQL Query, vertex 재귀호출
with recursive    
in_usa(vertex_id) AS (
        select vertex_id 
        from vertices 
        where properties->>'name' = 'US'
    UNION
        select edges.tail_vertex
        from edges
        join in_usa 
        on edges.head_vertex = in_usa.vertex_id
        where edges.label = 'within'
),

in_europe(vertex_id) as (
        select vertex_id 
        from vertices 
        where properties->>'name' = 'Europe'
    UNION
        select edges.tail_vertex
        from edges
        join in_europe 
        on edges.head_vertex = in_europe.vertex_id
        where edges.label = 'within'
),

born_in_usa(vertex_id) as (
    select edges.tail_vertex
    from edges
    join in_usa on edges.head_vertex = in_usa.vertex_id
    where edges.label = 'born_in'
),

lives_in_europe(vertex_id) as (
    select edges.tail_vertex
    from edges
    join in_europe on edges.head_vertex = in_europe.vertex_id
    where edges.label = 'lives_in'
)

-- Cypher Query
MATCH 
    (person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name: 'US'}),
    (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (europe:Location {name: 'Europe'})
return person.name
