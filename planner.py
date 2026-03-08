from datetime import date, timedelta, datetime

def generate_study_plan(subjects, exam_date_str, daily_hours):
    try:
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        today = date.today()
        days_left = (exam_date - today).days
        
        if days_left < 1:
            return {"error": "Exam date must be in the future!"}
        
        # Create task list with priority (higher difficulty = higher priority)
        all_tasks = []
        for sub in subjects:
            diff = int(sub["difficulty"])
            topics = [t.strip() for t in sub["topics"].split(",") if t.strip()]
            for topic in topics:
                all_tasks.append({
                    "subject": sub["name"],
                    "topic": topic,
                    "hours": diff,          # difficulty = estimated hours (1-5)
                    "priority": diff
                })
        
        # Priority algorithm: sort by difficulty descending
        all_tasks.sort(key=lambda x: x["priority"], reverse=True)
        
        schedule = []
        task_idx = 0
        current_date = today
        
        for day in range(days_left):
            day_tasks = []
            hours_used = 0
            
            while task_idx < len(all_tasks) and hours_used < daily_hours:
                task = all_tasks[task_idx]
                if task["hours"] <= (daily_hours - hours_used):
                    day_tasks.append({
                        "subject": task["subject"],
                        "topic": task["topic"],
                        "hours": task["hours"]
                    })
                    hours_used += task["hours"]
                    task_idx += 1
                else:
                    break  # can't fit → next day
            
            day_str = f"Day {day + 1} ({current_date.strftime('%b %d')})"
            schedule.append({
                "day": day_str,
                "tasks": day_tasks,
                "hours_used": hours_used
            })
            current_date += timedelta(days=1)
        
        remaining = len(all_tasks) - task_idx
        result = {
            "schedule": schedule,
            "days_left": days_left,
            "total_topics": len(all_tasks),
            "remaining_topics": remaining
        }
        if remaining > 0:
            result["warning"] = f"{remaining} topics left. Increase daily hours!"
        return result
        
    except Exception as e:
        return {"error": str(e)}