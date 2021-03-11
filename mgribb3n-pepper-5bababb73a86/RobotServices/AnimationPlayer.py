# -*- coding: utf-8 -*-


class AnimationPlayer:
    def __init__(self, session):
        self.animation_player_service = session.service("ALAnimationPlayer")

    # Plays an animation, but doesn't return before
    # the animation is finished.
    def play_animation(self, animation_path):
        self.animation_player_service.run(animation_path)

    # Plays an animation and returns immediately .
    # Returns currently running animation.
    def play_animation_async(self, animation_path):
        return self.animation_player_service.run(animation_path, _async=True)

    # Plays a random animation in the given tag category,
    # but doesn't return before the animation is finished
    def play_tag_animation(self, tag):
        self.animation_player_service.runTag(tag)

    # Plays a random animation in the given tag category
    # and returns immediately .
    # Returns currently running animation.
    def play_tag_animation_async(self, tag):
        return self.animation_player_service.runTag(tag, _async=True)

    # Waits for a given animation to finish.
    def wait_for_animation(self, animation):
        animation.value()

    # Cancels a given animation.
    def cancel_animation(self, animation):
        animation.cancel()

    # Declares a path for custom tags.
    def declare_path_for_tags(self, tag_path):
        self.animation_player_service.declarePathForTags(tag_path)

    # Associates tags to animations.
    def associate_tag_to_animation(self, tag_animation_dict):
        self.animation_player_service.addTagForAnimations(tag_animation_dict)

    # Resets the animation library to default
    def reset_animation_library(self):
        self.animation_player_service.reset()