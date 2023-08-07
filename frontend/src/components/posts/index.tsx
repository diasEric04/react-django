import { Component } from '../tsc-types'
import { PostCard } from '../postCard'
import { usePostContext } from '../../contexts/PostContext'
import { useEffect } from 'react'

export const Posts : Component = () => {
    const {postState : {posts, loading}, actions : {setPosts, startGet, endGet}} = usePostContext()

    useEffect(() => {
        (async() => {
            startGet()
            const response = await fetch('/api/v1/get')
            const data = await response.json()
            setPosts(data)
            endGet()
        })()
    }, [setPosts, startGet, endGet])
    
    console.log(posts)

    if (loading) {
        return <p>LOADING...</p>
    }
    
    return (
        <section>
            {posts.length > 0 && (
                posts.map( (post_content) => (
                    <PostCard {...post_content} />
                ))
            )}
        </section>
    )
}