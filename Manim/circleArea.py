from manim import *

class circleArea(Scene):
    def construct(self):
        RADIUS_COLOR = DARK_BLUE
        CIRCUMFERENCE_COLOR = DARK_BLUE
        CIRCLE_FILL = BLUE_B
        global originalSectors

        sector = Sector()
        arc = Arc()
        
        # Custom transform function that also transforms the position and rotation of the Mobject
        def custom_transform(mob, alpha, initial_obj: VGroup, target_obj: VGroup):
            # Interpolate the shape
            new_mob = VGroup().interpolate(initial_obj, target_obj, alpha)

            # Interpolate the position
            start_pos = initial_obj.get_center()
            end_pos = target_obj.get_center()
            new_pos = start_pos * (1 - alpha) + end_pos * alpha
            new_mob.move_to(new_pos)

            print(start_pos==end_pos) # The positions are all equal right now. currently the animation does nothing

            if len(new_mob) > 0:
                # Interpolate the rotation
                start_angle = initial_obj[0].get_angle()
                end_angle = target_obj[0].get_angle()
                new_angle = start_angle * (1 - alpha) + end_angle * alpha
                new_mob.rotate(new_angle - new_mob[0].get_angle())
                
                mob.become(new_mob)

        # Line rotates and fans out into a circle
        def initiateCircle(mob, alpha):
            # Set the sector's angle proportional to the alpha value (0 to 2*PI)
            sector.become(Sector(outer_radius=2, angle=alpha * 2 * PI, fill_color=CIRCLE_FILL, fill_opacity=1, stroke_width=0, z_index=0))
            arc.become(Arc(radius=2, angle=alpha * 2 * PI, stroke_color=CIRCUMFERENCE_COLOR, stroke_width=6, fill_opacity=0, z_index=1))
        
        # Draw slice lines from the radius of the circle to the circumference of the circle
        def sliceLines(numSlices: int):
            lines = [] # List of slice lines
            length = 2 # Circle's radius (Length of slice line)
            dAngle = 2 * PI / numSlices # Angle increment for slices
            # Iterate for numSlices / 2 as slice lines are diameters (every slice creates twice as many sectors as the previous)
            for l in range(numSlices):
                start_point = ORIGIN
                end_point = [length * np.cos(l * dAngle), length * np.sin(l * dAngle), 0] # Pythagorean theorem
                lines.append(Line(start_point, end_point, stroke_color=RADIUS_COLOR, stroke_width=1, z_index=1))
            return lines

        # Create equal sectors to "slice" the circle into
        def createSectors(numSlices: int):
            sectors = VGroup() # Create VGroup for pulling all sectors away from the center
            length = 2 # Circle's radius
            dAngle = 2 * PI / numSlices # Angle increment for sector rotation
            # Create sectors and rotate them accordingly so they form their corresponding segment of the circle
            for numArc in range(numSlices):
                sector = Sector(outer_radius=length, angle = dAngle, fill_color=CIRCLE_FILL, fill_opacity=1, z_index=0, stroke_width=0)
                arc = Arc(radius=2, start_angle=numArc * dAngle, angle=dAngle, stroke_color=CIRCUMFERENCE_COLOR, stroke_width=6, fill_opacity=0, z_index=1)
                sector.rotate(numArc * dAngle, about_point=ORIGIN)
                vgroup = VGroup(sector, arc)
                sectors.add(vgroup)
            return sectors
        
        # Disperse the sectors outwards from the center of the circle
        def disperseSectors(sectors: List[Mobject], dist: int):
            animations = [] # List for each sector shift animation
            sectCnt = 0 # Counter for the next loop
            dAngle = 2 * PI / len(sectors) # Angle increment for each sector transform vector

            # Create a list of transformations for each sector
            for sector in sectors:
                # Transformation vector for each corresponding sector
                shift_vector = [dist * np.cos(dAngle / 2 + dAngle * sectCnt), dist * np.sin(dAngle / 2 + dAngle * sectCnt), 0]
                animation = ApplyMethod(sector.shift, shift_vector)
                animations.append(animation)
                sectCnt += 1
            return animations
        
        # Consolidate the sectors back into a circle
        def sectorsToCircle(sectors: List[Mobject]):
            animations = [] # List for each sector's animation
            for index in range(len(sectors)):
                animation = UpdateFromAlphaFunc(sectors[index], lambda mob, alpha: custom_transform(mob, alpha, initial_obj=sectors[index], target_obj=originalSectors[index]))
                animations.append(animation)
            return animations
        
        # Animate the rotation of the radius line and update the sector fill
        radius = Line([0, 0, 0], [2, 0, 0], stroke_color=CIRCLE_FILL, stroke_width=6)        
        self.play(Create(radius), run_time=0.6)
        self.play(LaggedStart(AnimationGroup(UpdateFromAlphaFunc(sector, initiateCircle), UpdateFromAlphaFunc(arc, initiateCircle)), FadeOut(radius, run_time=1), lag_ratio=0.1))
        
        self.remove(radius)

        areaLabel = MathTex("\\pi r^2", font_size=48, color=WHITE).move_to([0, 0, 0]) # Create the label for the area of the circle

        self.play(Write(areaLabel))
        self.wait(1)
        self.play(Unwrite(areaLabel))

        self.wait(1)

        pi_approx = MathTex("\\pi \\approx 3.14159\\ldots").move_to([-4, 3, 0])

        self.play(Write(pi_approx))

        self.wait(1)
        
        radius = Line([0, 0, 0], [2, 0, 0], stroke_color=RADIUS_COLOR, stroke_width=6) # Create the radius again with different color
        radiusLabel = MathTex("r", font_size=48, color=WHITE).next_to(radius, UP) # Position the radius label

        self.play(Create(radius))
        self.play(Write(radiusLabel))

        circumference = Line([-2 * PI, -2, 0], [2 * PI, -2, 0], stroke_color=CIRCUMFERENCE_COLOR, stroke_width=6, z_index=1) # Create the straight line for the circumference to "roll out" into
        group = VGroup(sector, radiusLabel, radius) # Group the mobjects to move up

        self.play(ReplacementTransform(arc, circumference), group.animate.shift([0, 1, 0])) # Move the circle (group) up while "unwrapping" the circumference

        circumLabel = MathTex("2\\pi r", font_size=48, color=WHITE).next_to(circumference, DOWN) # Create label for the circumference line

        self.play(Write(circumLabel))
        self.wait(1)
        self.play(Unwrite(circumLabel), Unwrite(radiusLabel), Unwrite(pi_approx), Uncreate(radius))

        arc = Arc(radius=2, angle=2 * PI, stroke_color=CIRCUMFERENCE_COLOR, stroke_width=6, fill_opacity=0, z_index=1) # Redefine arc (to reset the transform)

        self.play(ReplacementTransform(circumference, arc), group.animate.shift([0, -1, 0]))
        self.wait(2)

        sectors = createSectors(32) # List of sectors for the circle to be sliced into
        originalSectors = sectors # Keep a reference to the transform of each sector so the sliced sectors can revert back to a circle
        lines = sliceLines(32) # List of lines to denote each slice
        objects = self.mobjects # Create a list of all current objects to delete later

        for line in lines:
            self.add(line)
            self.wait(0.05)

        for sector in sectors:
            self.add(sector)
        
        self.remove(*objects) # Remove the circle after the slice lines and sectors are added (so the removal is unnoticable)

        fadeoutAnimations = [FadeOut(line, run_time=0.5) for line in lines]
        sectorAnimations = disperseSectors(sectors, 0.5)

        self.play(LaggedStart(AnimationGroup(*sectorAnimations), AnimationGroup(*fadeoutAnimations), lag_ratio=0.1))
        self.wait(2)

        returnAnimation = sectorsToCircle(sectors)
        self.play(*returnAnimation)
        self.wait(2)