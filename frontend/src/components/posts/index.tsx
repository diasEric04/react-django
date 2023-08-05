import { Component } from '../tsc-types'
import { PostCard } from '../postCard'
import { usePostContext } from '../../contexts/PostContext'

export const Posts : Component = () => {
    const {postState : {posts, loading}, actions : {get, post}} = usePostContext()
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