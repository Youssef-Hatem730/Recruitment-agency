# Recruitment-agency

## Company

**Smart Recruit AI** is a recruitment technology company that helps job seekers find suitable job opportunities while assisting HR teams in matching candidates with available positions more efficiently.

## Problem Statement

Recruiters receive a large number of CVs in different formats (PDF, DOCX, and TXT). Manually reviewing every CV and matching it with suitable job opportunities is time-consuming and repetitive.

This project automates that process by reading a candidate's CV, extracting relevant technical skills, and recommending the most suitable job from a collection of available positions.

## Why an Agent Instead of a Simple Script?

A simple script performs the same sequence of steps every time regardless of the situation.

An autonomous agent, however, can make decisions based on the current input. Depending on the implementation, it can:
- react using predefined rules,
- route requests to different workflows,
- reason about which actions to take,
- or reason while following safety and execution constraints.

This project demonstrates these different decision-making approaches through four autonomous agent architectures:
- Reactive Agent
- Routing Agent
- Unconstrained ReAct Agent
- Constrained ReAct Agent
