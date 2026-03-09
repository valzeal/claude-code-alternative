"""
Claude Code Alternative - User Feedback Integration (Phase 4)
Collect, manage, and analyze user feedback
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class FeedbackType(Enum):
    """Types of feedback"""
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    IMPROVEMENT = "improvement"
    QUESTION = "question"
    RATING = "rating"
    GENERAL = "general"


class FeedbackStatus(Enum):
    """Feedback status"""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    DEFERRED = "deferred"


class FeedbackPriority(Enum):
    """Feedback priority"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Feedback:
    """User feedback item"""
    id: str
    user_id: str
    type: FeedbackType
    status: FeedbackStatus
    priority: FeedbackPriority
    title: str
    description: str
    category: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    rating: Optional[int] = None  # For rating feedback (1-5)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class FeedbackManager:
    """Manage user feedback collection and processing"""

    def __init__(self):
        """Initialize feedback manager"""
        self.feedback: Dict[str, Feedback] = {}
        self.feedback_counter = 0
        self.categories: List[str] = [
            "code_analysis",
            "code_generation",
            "code_review",
            "debugging",
            "documentation",
            "performance",
            "ui/ux",
            "api",
            "integration",
            "general"
        ]
        self.stats = {
            'total_feedback': 0,
            'by_status': {},
            'by_type': {},
            'by_priority': {},
            'resolved_count': 0
        }

    def _generate_feedback_id(self) -> str:
        """Generate unique feedback ID"""
        self.feedback_counter += 1
        return f"FB-{self.feedback_counter:06d}"

    def submit_feedback(
        self,
        user_id: str,
        feedback_type: FeedbackType,
        title: str,
        description: str,
        priority: FeedbackPriority = FeedbackPriority.MEDIUM,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        rating: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, Optional[Feedback]]:
        """
        Submit new feedback

        Args:
            user_id: User identifier
            feedback_type: Type of feedback
            title: Feedback title
            description: Detailed description
            priority: Feedback priority
            category: Category
            tags: Optional tags
            rating: Optional rating (1-5)
            metadata: Optional metadata

        Returns:
            (success, message, feedback)
        """
        if not user_id:
            return False, "User ID is required", None

        if not title or not description:
            return False, "Title and description are required", None

        if rating is not None and (rating < 1 or rating > 5):
            return False, "Rating must be between 1 and 5", None

        if category and category not in self.categories:
            return False, f"Invalid category. Valid categories: {self.categories}", None

        feedback = Feedback(
            id=self._generate_feedback_id(),
            user_id=user_id,
            type=feedback_type,
            status=FeedbackStatus.NEW,
            priority=priority,
            title=title,
            description=description,
            category=category,
            tags=tags or [],
            rating=rating,
            metadata=metadata or {}
        )

        self.feedback[feedback.id] = feedback
        self._update_stats()

        return True, "Feedback submitted successfully", feedback

    def update_feedback_status(
        self,
        feedback_id: str,
        status: FeedbackStatus,
        assignee: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Update feedback status

        Args:
            feedback_id: Feedback ID
            status: New status
            assignee: Optional assignee
            comment: Optional comment

        Returns:
            (success, message)
        """
        feedback = self.feedback.get(feedback_id)
        if not feedback:
            return False, "Feedback not found"

        feedback.status = status
        feedback.updated_at = time.time()

        if assignee:
            feedback.assignee = assignee

        if status == FeedbackStatus.RESOLVED:
            feedback.resolved_at = time.time()
            self.stats['resolved_count'] += 1

        if comment:
            feedback.responses.append({
                'user': 'system',
                'comment': comment,
                'timestamp': time.time()
            })

        self._update_stats()
        return True, "Feedback status updated"

    def add_response(
        self,
        feedback_id: str,
        user: str,
        comment: str
    ) -> Tuple[bool, str]:
        """
        Add response to feedback

        Args:
            feedback_id: Feedback ID
            user: User responding
            comment: Response comment

        Returns:
            (success, message)
        """
        feedback = self.feedback.get(feedback_id)
        if not feedback:
            return False, "Feedback not found"

        feedback.responses.append({
            'user': user,
            'comment': comment,
            'timestamp': time.time()
        })
        feedback.updated_at = time.time()

        return True, "Response added successfully"

    def get_feedback(
        self,
        feedback_id: str
    ) -> Optional[Feedback]:
        """Get feedback by ID"""
        return self.feedback.get(feedback_id)

    def list_feedback(
        self,
        user_id: Optional[str] = None,
        feedback_type: Optional[FeedbackType] = None,
        status: Optional[FeedbackStatus] = None,
        priority: Optional[FeedbackPriority] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Feedback]:
        """
        List feedback with filters

        Args:
            user_id: Filter by user ID
            feedback_type: Filter by type
            status: Filter by status
            priority: Filter by priority
            category: Filter by category
            limit: Maximum results to return

        Returns:
            List of matching feedback
        """
        results = list(self.feedback.values())

        # Apply filters
        if user_id:
            results = [f for f in results if f.user_id == user_id]

        if feedback_type:
            results = [f for f in results if f.type == feedback_type]

        if status:
            results = [f for f in results if f.status == status]

        if priority:
            results = [f for f in results if f.priority == priority]

        if category:
            results = [f for f in results if f.category == category]

        # Sort by created date (newest first)
        results.sort(key=lambda f: f.created_at, reverse=True)

        # Apply limit
        if limit:
            results = results[:limit]

        return results

    def search_feedback(
        self,
        query: str,
        limit: Optional[int] = None
    ) -> List[Feedback]:
        """
        Search feedback by text

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching feedback
        """
        query_lower = query.lower()
        results = []

        for feedback in self.feedback.values():
            # Search in title and description
            if query_lower in feedback.title.lower() or query_lower in feedback.description.lower():
                results.append(feedback)
                continue

            # Search in responses
            for response in feedback.responses:
                if query_lower in response.get('comment', '').lower():
                    results.append(feedback)
                    break

        # Sort by relevance (simple: by date)
        results.sort(key=lambda f: f.created_at, reverse=True)

        if limit:
            results = results[:limit]

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        return {
            **self.stats,
            'categories': self.categories,
            'total_resolved_rate': (
                self.stats['resolved_count'] / self.stats['total_feedback']
                if self.stats['total_feedback'] > 0
                else 0.0
            )
        }

    def _update_stats(self) -> None:
        """Update internal statistics"""
        all_feedback = list(self.feedback.values())

        self.stats['total_feedback'] = len(all_feedback)

        # Count by status
        self.stats['by_status'] = {}
        for status in FeedbackStatus:
            count = len([f for f in all_feedback if f.status == status])
            self.stats['by_status'][status.value] = count

        # Count by type
        self.stats['by_type'] = {}
        for ftype in FeedbackType:
            count = len([f for f in all_feedback if f.type == ftype])
            self.stats['by_type'][ftype.value] = count

        # Count by priority
        self.stats['by_priority'] = {}
        for priority in FeedbackPriority:
            count = len([f for f in all_feedback if f.priority == priority])
            self.stats['by_priority'][priority.value] = count

    def export_feedback(
        self,
        filepath: str,
        format: str = 'json'
    ) -> Tuple[bool, str]:
        """
        Export feedback to file

        Args:
            filepath: Output file path
            format: Export format (json, csv)

        Returns:
            (success, message)
        """
        try:
            if format == 'json':
                data = {
                    'feedback': [
                        {
                            **{k: v.value if isinstance(v, Enum) else v for k, v in f.__dict__.items()},
                            'type': f.type.value,
                            'status': f.status.value,
                            'priority': f.priority.value
                        }
                        for f in self.feedback.values()
                    ],
                    'stats': self.get_stats()
                }

                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

            elif format == 'csv':
                import csv

                with open(filepath, 'w', newline='') as f:
                    fieldnames = [
                        'id', 'user_id', 'type', 'status', 'priority',
                        'title', 'description', 'category', 'created_at',
                        'updated_at', 'resolved_at', 'assignee', 'rating'
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for feedback in self.feedback.values():
                        row = {
                            'id': feedback.id,
                            'user_id': feedback.user_id,
                            'type': feedback.type.value,
                            'status': feedback.status.value,
                            'priority': feedback.priority.value,
                            'title': feedback.title,
                            'description': feedback.description,
                            'category': feedback.category or '',
                            'created_at': feedback.created_at,
                            'updated_at': feedback.updated_at,
                            'resolved_at': feedback.resolved_at or '',
                            'assignee': feedback.assignee or '',
                            'rating': feedback.rating or ''
                        }
                        writer.writerow(row)

            return True, f"Feedback exported to {filepath}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"

    def get_trending_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get trending issues (most reported bugs)

        Args:
            limit: Maximum results

        Returns:
            List of trending issues
        """
        bug_reports = [
            f for f in self.feedback.values()
            if f.type == FeedbackType.BUG_REPORT
        ]

        # Group by similar titles (simple grouping)
        title_groups: Dict[str, List[Feedback]] = {}
        for feedback in bug_reports:
            # Normalize title (lowercase, remove special chars)
            normalized = feedback.title.lower().replace(' ', '')
            if normalized not in title_groups:
                title_groups[normalized] = []
            title_groups[normalized].append(feedback)

        # Sort by report count
        trending = sorted(
            title_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        result = []
        for normalized, reports in trending[:limit]:
            result.append({
                'title': reports[0].title,
                'count': len(reports),
                'feedback_ids': [f.id for f in reports],
                'latest_report': max(reports, key=lambda f: f.created_at)
            })

        return result

    def get_average_rating(self, feedback_type: Optional[FeedbackType] = None) -> Optional[float]:
        """
        Get average rating

        Args:
            feedback_type: Filter by feedback type

        Returns:
            Average rating or None
        """
        ratings = [
            f.rating for f in self.feedback.values()
            if f.rating is not None and
            (feedback_type is None or f.type == feedback_type)
        ]

        if not ratings:
            return None

        return sum(ratings) / len(ratings)


# Example usage
if __name__ == "__main__":
    manager = FeedbackManager()

    # Submit feedback
    success, message, feedback = manager.submit_feedback(
        user_id="user123",
        feedback_type=FeedbackType.BUG_REPORT,
        title="Code analysis returns incorrect complexity",
        description="The cyclomatic complexity calculation is returning wrong values for nested if statements.",
        priority=FeedbackPriority.HIGH,
        category="code_analysis",
        tags=["bug", "complexity"],
        metadata={"language": "python", "version": "1.0.0"}
    )
    print(f"Submit feedback: {success}, {message}")
    if feedback:
        print(f"Feedback ID: {feedback.id}")

    # Submit rating
    success, message, rating = manager.submit_feedback(
        user_id="user123",
        feedback_type=FeedbackType.RATING,
        title="Overall rating",
        description="Great tool, very helpful!",
        rating=5,
        category="general"
    )
    print(f"\nSubmit rating: {success}, {message}")

    # Submit feature request
    success, message, feature = manager.submit_feedback(
        user_id="user456",
        feedback_type=FeedbackType.FEATURE_REQUEST,
        title="Add support for Ruby",
        description="Please add support for Ruby language in code analysis.",
        priority=FeedbackPriority.MEDIUM,
        category="code_analysis",
        tags=["feature", "language_support"]
    )
    print(f"Submit feature request: {success}, {message}")

    # Update feedback status
    success, message = manager.update_feedback_status(
        feedback_id=feedback.id,
        status=FeedbackStatus.ACKNOWLEDGED,
        assignee="dev1",
        comment="Thank you for the feedback. We're investigating the issue."
    )
    print(f"\nUpdate status: {success}, {message}")

    # Add response
    success, message = manager.add_response(
        feedback_id=feedback.id,
        user="user123",
        comment="I have more details to share about this bug."
    )
    print(f"Add response: {success}, {message}")

    # List feedback
    all_feedback = manager.list_feedback(limit=10)
    print(f"\nTotal feedback: {len(all_feedback)}")
    for f in all_feedback[:3]:
        print(f"  {f.id}: {f.title} ({f.status.value})")

    # Search feedback
    results = manager.search_feedback("Ruby", limit=5)
    print(f"\nSearch results for 'Ruby': {len(results)}")
    for f in results:
        print(f"  {f.id}: {f.title}")

    # Get stats
    stats = manager.get_stats()
    print(f"\nFeedback stats: {json.dumps(stats, indent=2)}")

    # Get trending issues
    trending = manager.get_trending_issues(limit=5)
    print(f"\nTrending issues: {len(trending)}")
    for issue in trending:
        print(f"  {issue['title']}: {issue['count']} reports")

    # Get average rating
    avg_rating = manager.get_average_rating()
    print(f"\nAverage rating: {avg_rating:.1f}" if avg_rating else "No ratings yet")

    # Export feedback
    success, message = manager.export_feedback('/tmp/feedback_export.json', 'json')
    print(f"\nExport feedback: {success}, {message}")
