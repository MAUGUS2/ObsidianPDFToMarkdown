# {{ title }}
{{ lesson_description }}

---

## Themes
{% for theme in themes %}
### {{ theme.name }}
{{ theme.description }}

- **Topics:**
  {% for topic in theme.topics %}
  - **{{ topic.name }}**: {{ topic.description }}
  {% endfor %}

  {{ theme.content }}
  { Use the Obsidian formatting tools that best fit this theme to enhance visual content. }

  {% for topic in theme.topics %}
  #### {{ topic.name }}
  {{ topic.description }}

  - **Subtopics:**
    {% for subtopic in topic.subtopics %}
    - **{{ subtopic.name }}**: {{ subtopic.description }}
    {% endfor %}

  {{ topic.content }}
  { Use the Obsidian formatting tools that best fit this topic to enhance visual content. }

  {% for subtopic in topic.subtopics %}
  ##### {{ subtopic.name }}
  {{ subtopic.description }}

  {{ subtopic.content }}
  { Use the Obsidian formatting tools that best fit this subtopic to enhance visual content. }

  **Practical Examples:**
  {{ subtopic.practical_examples }}

  > [!tip] **Tip:**
  > {{ subtopic.tip }}

  > [!info] **Notice:**
  {{ subtopic.notice | default('No additional notice') }}

  **Applied Study Techniques:**
  - **Active learning:** {{ subtopic.techniques.active_learning | default('Not applied') }}
  - **Spaced repetition:** {{ subtopic.techniques.spaced_repetition | default('Not applied') }}
  - **Interleaved practice:** {{ subtopic.techniques.interleaved_practice | default('Not applied') }}
  - **Self-testing:** {{ subtopic.techniques.self_testing | default('Not applied') }}
  - **Concept mapping:** {{ subtopic.techniques.concept_mapping | default('Not applied') }}
  - **Dual coding:** {{ subtopic.techniques.dual_coding | default('Not applied') }}
  - **Elaboration:** {{ subtopic.techniques.elaboration | default('Not applied') }}
  - **Distraction management:** {{ subtopic.techniques.distraction_management | default('Not applied') }}
  - **Error review:** {{ subtopic.techniques.error_review | default('Not applied') }}
  - **Deep work:** {{ subtopic.techniques.deep_work | default('Not applied') }}

  {% endfor %}
  {% endfor %}
{% endfor %}

---

## Lesson Conclusion
{{ lesson_conclusion }}

---

## References and Recommended Readings
{{ references_and_readings }}
