import reflex as rx


def text_wrapper(title: str, description: str):
    return rx.vstack(
        rx.hstack(
            rx.text(
                title,
                size="4",
                weight="bold",
                color=rx.color("slate", 12),
            ),
            align="center",
        ),
        rx.text(description, size="3", color=rx.color("slate", 11), weight="medium"),
        spacing="2",
        line_height="2px",
    )


def reflexui():
    return rx.box(
        rx.vstack(
            text_wrapper(
                "What is ReflexUI?",
                "ReflexUI refers to ui components created by reflex. It's a collection of user interface components that are designed to simplify the decision-making process when it comes to designing and building user interfaces. One of his most famous thought experiments is the 'indian' paradox, which illustrates the challenges of decision-making in the face of equally appealing choices.",
            ),
            text_wrapper(
                "Why ReflexUI?",
                "I chose the name 'ReflexUI' to evoke the spirit of thoughtful decision-making in design. Just as Buridan's donkey faced a dilemma between two equally appealing bales of hay, developers often grapple with choices in component design and user experience. This site aims to provide a clear path through those choices by offering beautifully crafted, reusable components that simplify the decision-making process.",
            ),
            text_wrapper(
                "Explore and Create",
                "Dive into our collection of components and see how they can elevate your projects. Whether you’re building a new app or enhancing an existing one, Buridan UI is here to help you navigate the vast landscape of design choices with ease.",
            ),
            max_width="50em",
            width="100%",
            spacing="6",
        ),
        width="100%",
        display="flex",
        justify_content="center",
        padding="0px 14px",
    )
