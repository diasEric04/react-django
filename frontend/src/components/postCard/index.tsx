import { PostCardType } from "../tsc-types"

export const PostCard : PostCardType = ({ title, description, author, content}) => {
    return (
        <article>
            <h3>{title}</h3>
            <small>{description} <b><i>{author}</i></b></small>
            <hr />
            {content}
        </article>
    )
}